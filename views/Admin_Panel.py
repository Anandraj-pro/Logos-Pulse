import streamlit as st
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id, DEFAULT_PASSWORDS
from modules.rbac import (
    create_account, get_users_by_role, get_pastors_list, get_bishops_list,
    reset_user_password, delete_account
)
from modules.supabase_client import get_admin_client

require_role(["admin"])

inject_styles()

page_header("\U0001f6e1\ufe0f", "Admin Panel", "Manage users, roles, and platform settings")

tab_users, tab_create, tab_bulk, tab_announce, tab_audit, tab_analytics, tab_reminders, tab_export = st.tabs([
    "\U0001f465 All Users", "\u2795 Create Account", "\U0001f4e4 Bulk Import",
    "\U0001f4e2 Announcements", "\U0001f4dc Audit Log", "\U0001f4ca Analytics", "\u23f0 Reminders", "\U0001f4e5 Export"
])

# ==================== ALL USERS ====================
with tab_users:
    # Role filter
    col_filter, col_search = st.columns([1, 2])
    with col_filter:
        role_filter = st.selectbox(
            "Filter by Role",
            ["All", "Admin", "Bishop", "Pastor", "Prayer Warrior"],
            label_visibility="collapsed",
        )
    with col_search:
        search_query = st.text_input("Search", placeholder="Search by name or email...", label_visibility="collapsed")

    # Fetch users
    admin = get_admin_client()
    if role_filter == "All":
        result = admin.table("user_profiles").select("*").execute()
    else:
        role_key = role_filter.lower().replace(" ", "_")
        result = admin.table("user_profiles").select("*").eq("role", role_key).execute()

    profiles = result.data or []

    # Enrich with auth user data
    users_display = []
    for profile in profiles:
        try:
            user_resp = admin.auth.admin.get_user_by_id(profile["user_id"])
            user = user_resp.user
            meta = user.user_metadata or {}
            users_display.append({
                "user_id": profile["user_id"],
                "email": user.email,
                "first_name": meta.get("first_name", ""),
                "last_name": meta.get("last_name", ""),
                "preferred_name": meta.get("preferred_name", ""),
                "role": profile["role"],
                "membership_card_id": profile.get("membership_card_id", ""),
                "must_change_password": profile.get("must_change_password", False),
                "created_at": profile.get("created_at", ""),
            })
        except Exception:
            continue

    # Apply search filter
    if search_query:
        q = search_query.lower()
        users_display = [u for u in users_display if (
            q in u["email"].lower()
            or q in u["first_name"].lower()
            or q in u["last_name"].lower()
            or q in u["preferred_name"].lower()
            or q in (u.get("membership_card_id") or "").lower()
        )]

    st.caption(f"{len(users_display)} user(s)")

    if not users_display:
        empty_state("\U0001f465", "No users found")
    else:
        role_colors = {
            "admin": "#C44B5B",
            "bishop": "#2196F3",
            "pastor": "#3A8F5C",
            "prayer_warrior": "#5B4FC4",
        }
        role_bgs = {
            "admin": "#FFEBEE",
            "bishop": "#E3F2FD",
            "pastor": "#E8F5E9",
            "prayer_warrior": "#EDEBFA",
        }

        for user in users_display:
            role = user["role"]
            r_color = role_colors.get(role, "#888")
            r_bg = role_bgs.get(role, "#F5F5F5")
            r_label = role.replace("_", " ").title()
            pw_flag = " \U0001f534" if user["must_change_password"] else ""
            card_info = f" | Card: {user['membership_card_id']}" if user.get("membership_card_id") else ""

            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">
                            {user['preferred_name'] or user['first_name']} {user['last_name']}
                        </span>
                        <span style="background:{r_bg}; color:{r_color}; padding:2px 10px;
                                     border-radius:10px; font-size:11px; font-weight:600; margin-left:8px;">
                            {r_label}
                        </span>
                        {f'<span style="font-size:11px; color:#C44B5B; margin-left:6px;" title="Must change password">{pw_flag}</span>' if pw_flag else ''}
                    </div>
                    <div style="font-size:12px; color:#9E96AB;">
                        {user['created_at'][:10] if user['created_at'] else ''}
                    </div>
                </div>
                <div style="font-size:13px; color:#6B6580; margin-top:4px;">
                    {user['email']}{card_info}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            col_reset, col_del = st.columns([1, 1])
            with col_reset:
                if st.button(f"Reset Password", key=f"reset_{user['user_id']}", use_container_width=True):
                    result = reset_user_password(user["user_id"], user["role"])
                    if result["success"]:
                        st.success(f"Password reset to **{DEFAULT_PASSWORDS.get(role, 'Open@123')}**")
                    else:
                        st.error(result["error"])
            with col_del:
                if user["role"] != "admin":
                    if st.button("Delete", key=f"del_{user['user_id']}", use_container_width=True):
                        st.session_state[f"confirm_del_user_{user['user_id']}"] = True

                    if st.session_state.get(f"confirm_del_user_{user['user_id']}"):
                        st.warning(f"Delete **{user['email']}**? This removes all their data permanently.")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("Yes, Delete", key=f"yes_del_{user['user_id']}", type="primary"):
                                result = delete_account(user["user_id"])
                                if result["success"]:
                                    st.session_state.pop(f"confirm_del_user_{user['user_id']}", None)
                                    st.success("Account deleted.")
                                    st.rerun()
                                else:
                                    st.error(result["error"])
                        with c2:
                            if st.button("Cancel", key=f"no_del_{user['user_id']}"):
                                st.session_state.pop(f"confirm_del_user_{user['user_id']}", None)
                                st.rerun()

# ==================== CREATE ACCOUNT ====================
with tab_create:
    section_label("Create a New Account")

    st.markdown("""
    <div style="font-size:13px; color:#9E96AB; margin-bottom:16px;">
        Create Bishop, Pastor, or Prayer Warrior accounts. Each role gets a default password
        that must be changed on first login.
    </div>
    """, unsafe_allow_html=True)

    with st.form("create_account_form"):
        new_role = st.selectbox("Role", ["bishop", "pastor", "prayer_warrior"],
                                format_func=lambda x: x.replace("_", " ").title())

        new_email = st.text_input("Email", placeholder="user@email.com")

        col1, col2 = st.columns(2)
        with col1:
            new_first = st.text_input("First Name")
        with col2:
            new_last = st.text_input("Last Name")

        new_card = st.text_input("Church Membership Card ID (optional)", placeholder="e.g. TKT1694")

        # Conditional fields based on role
        bishop_id = None
        pastor_id = None
        region = ""

        if new_role == "pastor":
            bishops = get_bishops_list()
            if bishops:
                bishop_options = {b["display_name"] + f" ({b['email']})": b["user_id"] for b in bishops}
                selected_bishop = st.selectbox("Assign to Bishop", options=list(bishop_options.keys()))
                bishop_id = bishop_options.get(selected_bishop)
            else:
                st.info("No bishops yet. Pastor will not be assigned to a bishop.")
            region = st.text_input("Region / Group (optional)")

        elif new_role == "prayer_warrior":
            pastors = get_pastors_list()
            if pastors:
                pastor_options = {p["display_name"] + f" ({p['email']})": p["user_id"] for p in pastors}
                selected_pastor = st.selectbox("Assign to Pastor", options=list(pastor_options.keys()))
                pastor_id = pastor_options.get(selected_pastor)
            else:
                st.warning("No pastors available. Create a Pastor account first.")

        prayer_bench = st.number_input("Prayer Benchmark (minutes)", min_value=15, max_value=480, value=60, step=15)

        create_submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

    if create_submitted:
        if not new_email or not new_first or not new_last:
            st.error("Please fill in email, first name, and last name.")
        elif new_role == "prayer_warrior" and not pastor_id:
            st.error("Please select a pastor for this Prayer Warrior.")
        else:
            with st.spinner("Creating account..."):
                result = create_account(
                    email=new_email.strip().lower(),
                    first_name=new_first.strip(),
                    last_name=new_last.strip(),
                    role=new_role,
                    created_by=get_current_user_id(),
                    pastor_id=pastor_id,
                    bishop_id=bishop_id,
                    prayer_benchmark=prayer_bench,
                    membership_card_id=new_card.strip() if new_card else None,
                    region_or_group=region.strip() if region else "",
                )

            if result["success"]:
                default_pw = DEFAULT_PASSWORDS.get(new_role, "Open@123")
                st.success(f"Account created for **{new_email}**")
                st.info(f"Default password: **{default_pw}** (must change on first login)")

                # Seed data for prayer warriors
                if new_role == "prayer_warrior":
                    from modules.seed import seed_user_data
                    with st.spinner("Seeding default data..."):
                        seed_user_data(result["user_id"], new_first.strip(), prayer_bench)
                    st.success("Default prayer categories and prayers seeded.")
            else:
                st.error(result["error"])

# ==================== BULK IMPORT ====================
with tab_bulk:
    section_label("Bulk Account Creation via CSV")

    st.markdown("""
    <div style="font-size:13px; color:#9E96AB; margin-bottom:16px;">
        Upload a CSV file to create multiple accounts at once.
        Each row creates one account with the role-specific default password.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **CSV Format** (columns):
    | email | first_name | last_name | role | pastor_email | membership_card_id |
    |-------|-----------|-----------|------|-------------|-------------------|
    | john@example.com | John | Doe | prayer_warrior | pastor@example.com | TKT001 |
    """)

    st.caption("Roles: `bishop`, `pastor`, `prayer_warrior`. The `pastor_email` column is required for prayer_warrior accounts. `membership_card_id` is optional.")

    # Download template
    csv_template = "email,first_name,last_name,role,pastor_email,membership_card_id\njohn@example.com,John,Doe,prayer_warrior,pastor@example.com,TKT001\njane@example.com,Jane,Smith,prayer_warrior,pastor@example.com,TKT002\n"
    st.download_button("Download CSV Template", data=csv_template, file_name="logos_pulse_accounts_template.csv",
                       mime="text/csv", use_container_width=True)

    spacer()

    uploaded_csv = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_csv:
        import csv
        import io

        content = uploaded_csv.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)

        if not rows:
            st.error("CSV is empty.")
        else:
            st.success(f"Found **{len(rows)}** account(s) to create.")

            # Validate
            errors = []
            # Build pastor email -> ID lookup
            pastors = get_pastors_list()
            pastor_lookup = {p["email"].lower(): p["user_id"] for p in pastors}

            bishops = get_bishops_list()
            bishop_lookup = {b["email"].lower(): b["user_id"] for b in bishops}

            valid_rows = []
            for i, row in enumerate(rows, 1):
                email = (row.get("email") or "").strip().lower()
                first = (row.get("first_name") or "").strip()
                last = (row.get("last_name") or "").strip()
                role = (row.get("role") or "").strip().lower()
                pastor_email = (row.get("pastor_email") or "").strip().lower()
                card = (row.get("membership_card_id") or "").strip()

                if not email or not first or not last:
                    errors.append(f"Row {i}: Missing email, first_name, or last_name")
                    continue
                if role not in ("bishop", "pastor", "prayer_warrior"):
                    errors.append(f"Row {i}: Invalid role '{role}'")
                    continue
                if role == "prayer_warrior" and pastor_email not in pastor_lookup:
                    errors.append(f"Row {i}: Pastor '{pastor_email}' not found")
                    continue

                valid_rows.append({
                    "email": email, "first_name": first, "last_name": last,
                    "role": role, "pastor_id": pastor_lookup.get(pastor_email),
                    "bishop_id": bishop_lookup.get(pastor_email),
                    "membership_card_id": card or None,
                })

            if errors:
                for e in errors:
                    st.warning(e)

            if valid_rows:
                st.info(f"**{len(valid_rows)}** valid account(s) ready to create. {len(errors)} error(s).")

                if st.button(f"Create {len(valid_rows)} Accounts", type="primary", use_container_width=True):
                    admin_id = get_current_user_id()
                    created = 0
                    failed = 0

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i, row in enumerate(valid_rows):
                        status_text.text(f"Creating {row['email']}... ({i+1}/{len(valid_rows)})")
                        result = create_account(
                            email=row["email"],
                            first_name=row["first_name"],
                            last_name=row["last_name"],
                            role=row["role"],
                            created_by=admin_id,
                            pastor_id=row.get("pastor_id"),
                            bishop_id=row.get("bishop_id"),
                            membership_card_id=row.get("membership_card_id"),
                        )
                        if result.get("success"):
                            created += 1
                        else:
                            failed += 1
                            st.warning(f"{row['email']}: {result.get('error', 'Failed')}")
                        progress_bar.progress((i + 1) / len(valid_rows))

                    status_text.empty()
                    progress_bar.empty()
                    st.success(f"Done! Created: {created}, Failed: {failed}")
                    if created > 0:
                        st.rerun()

# ==================== ANNOUNCEMENTS ====================
with tab_announce:
    from modules import db as _db

    section_label("Create Announcement")

    with st.form("announcement_form"):
        ann_title = st.text_input("Title", placeholder="e.g., App Maintenance Tonight")
        ann_msg = st.text_area("Message", height=100, placeholder="Details about the announcement...")
        ann_role = st.selectbox("Target Audience", ["all", "prayer_warrior", "pastor", "bishop"],
                                format_func=lambda x: x.replace("_", " ").title())
        ann_submit = st.form_submit_button("Publish Announcement", type="primary", use_container_width=True)

    if ann_submit:
        if ann_title.strip() and ann_msg.strip():
            _db.create_announcement(ann_title.strip(), ann_msg.strip(), ann_role)
            _db.log_audit("announcement.created", target_type="announcement",
                          details={"title": ann_title.strip(), "target_role": ann_role})
            st.success("Announcement published!")
            st.rerun()
        else:
            st.error("Please fill in title and message.")

    spacer()
    section_label("Active Announcements")
    _all_ann = admin.table("announcements").select("*").eq("is_active", True).order("created_at", desc=True).execute()
    for a in (_all_ann.data or []):
        st.markdown(f"""
        <div class="entry-card">
            <div style="font-weight:600; color:#2A2438;">\U0001f4e2 {a['title']}</div>
            <div style="font-size:13px; color:#6B6580; margin-top:4px;">{a['message']}</div>
            <div style="font-size:11px; color:#9E96AB; margin-top:4px;">
                Target: {a.get('target_role', 'all').replace('_',' ').title()} | {(a.get('created_at') or '')[:10]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Deactivate", key=f"deact_{a['id']}", use_container_width=True):
            admin.table("announcements").update({"is_active": False}).eq("id", a["id"]).execute()
            _db.log_audit("announcement.removed", target_type="announcement",
                          target_id=str(a["id"]), details={"title": a["title"]})
            st.rerun()

# ==================== AUDIT LOG ====================
with tab_audit:
    _ACTION_META = {
        "user.created":          ("#3A8F5C", "#E8F5E9",  "\ud83d\udc64 Created"),
        "user.deleted":          ("#C44B5B", "#FFEBEE",  "\ud83d\uddd1\ufe0f Deleted"),
        "user.password_reset":   ("#D4853A", "#FFF3E0",  "\ud83d\udd11 Pwd Reset"),
        "announcement.created":  ("#5B4FC4", "#EDEBFA",  "\ud83d\udce2 Announced"),
        "announcement.removed":  ("#9E96AB", "#F5F3FA",  "\ud83d\udced Ann. Removed"),
    }

    audit_all = _db.get_audit_log(limit=200)

    col_af, col_sf = st.columns([2, 3])
    with col_af:
        action_options = ["All"] + sorted({e["action"] for e in audit_all})
        action_filter = st.selectbox("Filter by action", action_options, label_visibility="collapsed")
    with col_sf:
        search_actor = st.text_input("Search by name", placeholder="Actor name\u2026", label_visibility="collapsed")

    audit_entries = [
        e for e in audit_all
        if (action_filter == "All" or e["action"] == action_filter)
        and (not search_actor or search_actor.lower() in e.get("actor_name", "").lower())
    ]

    st.markdown(f"""
    <div style="font-size:12px; color:#9E96AB; margin-bottom:8px;">
        Showing {len(audit_entries)} of {len(audit_all)} entries
    </div>
    """, unsafe_allow_html=True)

    if not audit_entries:
        empty_state("\U0001f4dc", "No audit entries yet", "Actions will be logged as users interact with the system")
    else:
        for entry in audit_entries:
            action = entry.get("action", "")
            color, bg, label = _ACTION_META.get(action, ("#9E96AB", "#F5F3FA", action))
            log_date = (entry.get("created_at") or "")[:19].replace("T", " ")
            details = entry.get("details") or {}
            detail_parts = [f"{k}: {v}" for k, v in details.items() if v is not None]
            detail_str = " &nbsp;\u00b7&nbsp; ".join(detail_parts)

            st.markdown(f"""
            <div class="entry-card" style="padding:10px 14px; margin-bottom:4px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span style="background:{bg}; color:{color}; font-size:11px; font-weight:600;
                                     padding:2px 8px; border-radius:8px; white-space:nowrap;">
                            {label}
                        </span>
                        <span style="font-size:13px; color:#2A2438; font-weight:500;">
                            {entry.get('actor_name', 'System')}
                        </span>
                    </div>
                    <span style="font-size:11px; color:#C0B8CC; white-space:nowrap; margin-left:12px;">
                        {log_date}
                    </span>
                </div>
                {f'<div style="font-size:12px; color:#9E96AB; margin-top:4px;">{detail_str}</div>' if detail_str else ""}
            </div>
            """, unsafe_allow_html=True)

# ==================== ANALYTICS ====================
with tab_analytics:
    section_label("Platform Overview")

    admin = get_admin_client()

    # Count by role
    all_profiles = admin.table("user_profiles").select("role").execute()
    profiles_data = all_profiles.data or []

    counts = {"admin": 0, "bishop": 0, "pastor": 0, "prayer_warrior": 0}
    for p in profiles_data:
        r = p.get("role", "")
        if r in counts:
            counts[r] += 1

    total = sum(counts.values())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:#2A2438;">{total}</div>
            <div class="stat-label">Total Users</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:#2196F3;">{counts['bishop']}</div>
            <div class="stat-label">Bishops</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:#3A8F5C;">{counts['pastor']}</div>
            <div class="stat-label">Pastors</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:#5B4FC4;">{counts['prayer_warrior']}</div>
            <div class="stat-label">Prayer Warriors</div>
        </div>
        """, unsafe_allow_html=True)

    spacer()

    # Today's activity
    section_label("Today's Activity")
    from datetime import date
    today_str = date.today().isoformat()

    today_entries = admin.table("daily_entries") \
        .select("user_id", count="exact") \
        .eq("date", today_str) \
        .execute()
    logged_today = today_entries.count or 0

    pw_count = counts["prayer_warrior"]
    login_pct = int(logged_today / pw_count * 100) if pw_count > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:#3A8F5C;">{logged_today}</div>
            <div class="stat-label">Logged Today</div>
            <div style="font-size:11px; color:#C0B8CC; margin-top:2px;">out of {pw_count} warriors</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        pct_color = "#3A8F5C" if login_pct >= 70 else "#D4853A" if login_pct >= 40 else "#C44B5B"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:{pct_color};">{login_pct}%</div>
            <div class="stat-label">Engagement Rate</div>
        </div>
        """, unsafe_allow_html=True)

    # Pending password changes
    spacer()
    section_label("Pending Password Changes")
    pending = admin.table("user_profiles") \
        .select("user_id, role", count="exact") \
        .eq("must_change_password", True) \
        .execute()
    pending_count = pending.count or 0

    if pending_count > 0:
        st.warning(f"{pending_count} user(s) still using default passwords.")
    else:
        st.success("All users have updated their passwords.")

    # ==================== WEEKLY DIGEST ====================
    spacer()
    section_label("Weekly Digest Email")

    from modules.email_sender import is_configured
    from modules.digest import build_all_digests, format_digest_email

    if not is_configured():
        st.info(
            "Email not configured. Add an **[email]** section to `.streamlit/secrets.toml`:\n\n"
            "```toml\n[email]\n"
            "smtp_host     = \"smtp.gmail.com\"\n"
            "smtp_port     = 587\n"
            "smtp_user     = \"your@gmail.com\"\n"
            "smtp_password = \"your-app-password\"\n"
            "from_name     = \"Logos Pulse\"\n```"
        )
    else:
        st.caption("Send each Prayer Warrior their weekly summary (streak, chapters, confessions).")

        # Test email
        from modules.email_sender import send_email
        _admin_email = st.secrets.get("email", {}).get("smtp_user", "")
        if st.button(f"Send Test Email to {_admin_email}", use_container_width=True):
            result = send_email(
                _admin_email,
                "Logos Pulse — Email Test",
                "This is a test email from Logos Pulse.\n\nIf you received this, Gmail SMTP is working correctly."
            )
            if result["success"]:
                st.success(f"Test email sent to {_admin_email}!")
            else:
                st.error(f"Failed: {result['error']}")

        spacer(8)

        if "digest_preview" not in st.session_state:
            if st.button("Preview Digest", use_container_width=True):
                with st.spinner("Building digest…"):
                    st.session_state["digest_preview"] = build_all_digests()
                st.rerun()

        if "digest_preview" in st.session_state:
            previews = st.session_state["digest_preview"]
            st.markdown(f"**{len(previews)} recipient(s)** will receive this digest:")

            for d in previews[:5]:
                subject, body = format_digest_email(d)
                with st.expander(f"{d['display_name']} — {d['email']}"):
                    st.code(body, language=None)

            if len(previews) > 5:
                st.caption(f"… and {len(previews) - 5} more.")

            col_send, col_cancel = st.columns(2)
            with col_send:
                if st.button("Send to All", type="primary", use_container_width=True):
                    from modules.email_sender import send_bulk
                    recipients = []
                    for d in previews:
                        subject, body = format_digest_email(d)
                        recipients.append({"to": d["email"], "subject": subject, "body": body})

                    with st.spinner(f"Sending to {len(recipients)} members…"):
                        result = send_bulk(recipients)

                    _db.log_audit("digest.sent", target_type="digest",
                                  details={"sent": result["sent"], "failed": len(result["failed"])})
                    st.session_state.pop("digest_preview", None)

                    if result["failed"]:
                        st.warning(f"Sent {result['sent']}, failed {len(result['failed'])}: "
                                   + ", ".join(f["email"] for f in result["failed"]))
                    else:
                        st.success(f"Digest sent to {result['sent']} member(s)!")
                    st.rerun()

            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.pop("digest_preview", None)
                    st.rerun()

# ==================== DAILY REMINDERS ====================
with tab_reminders:
    import modules.db as _db2
    from modules.supabase_client import get_admin_client as _get_admin

    section_label("Daily Reminder System")
    st.caption(
        "When enabled, Logos Pulse sends a reminder email at 7:00 PM (IST) "
        "to Prayer Warriors who haven't logged their disciplines that day."
    )

    spacer(8)

    # Global on/off toggle
    _admin2 = _get_admin()
    _setting_row = _admin2.table("system_settings").select("value").eq("key", "reminders_enabled").execute()
    _reminders_on = (_setting_row.data[0]["value"] == "true") if _setting_row.data else True

    new_val = st.toggle("Daily reminders enabled", value=_reminders_on)
    if new_val != _reminders_on:
        _admin2.table("system_settings").upsert(
            {"key": "reminders_enabled", "value": "true" if new_val else "false", "updated_at": "now()"},
            on_conflict="key"
        ).execute()
        _db2.log_audit("system_setting.updated", target_type="system_settings",
                       details={"key": "reminders_enabled", "value": str(new_val)})
        st.success("Setting saved." if new_val else "Reminders disabled.")
        st.rerun()

    spacer(8)

    # Last run timestamp from audit_log
    section_label("Last Reminder Run")
    _last = _admin2.table("audit_log") \
        .select("created_at, details") \
        .eq("action", "reminder_email_sent") \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()

    if _last.data:
        _ts = _last.data[0]["created_at"][:19].replace("T", " ")
        _det = _last.data[0].get("details") or {}
        st.success(f"Last run: **{_ts} UTC**")
        if _det.get("sent"):
            st.caption(f"Sent {_det['sent']} reminder(s), failed {_det.get('failed', 0)}.")
    else:
        st.info("No reminder runs recorded yet.")

    spacer(8)

    # Setup instructions
    with st.expander("Setup: pg_cron + Edge Function"):
        st.markdown("""
**Step 1 — Deploy the Edge Function**
```bash
supabase functions deploy send-daily-reminders
supabase secrets set SMTP_HOST=smtp.gmail.com SMTP_PORT=587 \\
  SMTP_USER=your@gmail.com SMTP_PASSWORD=your-app-password \\
  FROM_NAME="Logos Pulse" \\
  APP_URL=https://logos-pulse.streamlit.app \\
  SUPABASE_URL=https://whyvlkkjbxehdbsgohre.supabase.co \\
  SUPABASE_SERVICE_ROLE_KEY=<service_role_key>
```

**Step 2 — Enable pg_cron**
Supabase Dashboard → Database → Extensions → **pg_cron** (enable)

**Step 3 — Schedule the job (run in SQL Editor)**
```sql
SELECT cron.schedule(
  'daily-reminders',
  '30 13 * * *',
  $$
    SELECT net.http_post(
      url := 'https://whyvlkkjbxehdbsgohre.supabase.co/functions/v1/send-daily-reminders',
      headers := jsonb_build_object(
        'Content-Type', 'application/json',
        'Authorization', 'Bearer <service_role_key>'
      ),
      body := '{}'::jsonb
    )
  $$
);
```
Replace `<service_role_key>` with the value from Supabase → Settings → API.
""")

    spacer(8)

    # ── Reading Plan Seed Data ──
    section_label("\U0001f4da Reading Plans — Seed Built-in Plans")
    st.caption("Insert the 3 built-in reading plans (NT in 90 Days, Psalms in 30 Days, Gospels in 28 Days). Safe to run multiple times — skips plans that already exist.")

    if st.button("\U0001f331 Seed Reading Plans", type="primary", key="seed_plans_btn"):
        try:
            from modules.seed_reading_plans import seed_reading_plans as _seed_plans
            result = _seed_plans()
            if result["inserted"] > 0:
                st.success(f"Seeded {result['inserted']} plan(s). {result['skipped']} already existed.")
            else:
                st.info(f"All {result['skipped']} plan(s) already seeded — nothing to do.")
        except Exception as e:
            st.error(f"Seed failed: {e}")

# ==================== EXPORT ====================
with tab_export:
    import csv, io
    from datetime import date as _date, timedelta as _td
    from modules.db import (
        get_member_activity_export, get_reading_completions_export, get_prayer_hours_export,
    )
    from modules.styles import section_label as _sec

    _sec("\U0001f4e5 Data Export")
    st.caption("Download member data as CSV for reporting, analysis, or pastoral oversight.")

    exp_type = st.selectbox("Export Type", [
        "Member Activity Log",
        "Reading Plan Progress",
        "Prayer Hours by Member",
    ], key="exp_type")

    exp_start = _date.today() - _td(days=30)
    exp_end = _date.today()
    if exp_type in ("Member Activity Log", "Prayer Hours by Member"):
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            exp_start = st.date_input("From", value=exp_start, key="exp_start")
        with col_d2:
            exp_end = st.date_input("To", value=exp_end, key="exp_end")

    if st.button("Generate Export", type="primary", use_container_width=True):
        try:
            buf = io.StringIO()

            if exp_type == "Member Activity Log":
                rows = get_member_activity_export(exp_start.isoformat(), exp_end.isoformat())
                if not rows:
                    st.info("No entries in that date range.")
                else:
                    writer = csv.DictWriter(buf, fieldnames=["date", "display_name", "role", "prayer_minutes", "chapters_display", "sermons_count"])
                    writer.writeheader()
                    for r in rows:
                        writer.writerow({k: r.get(k, "") for k in writer.fieldnames})
                    st.download_button(
                        "\U0001f4e5 Download Member Activity CSV",
                        data=buf.getvalue(),
                        file_name=f"member_activity_{exp_start}_{exp_end}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                    st.success(f"{len(rows)} entries ready.")

            elif exp_type == "Reading Plan Progress":
                rows = get_reading_completions_export()
                if not rows:
                    st.info("No reading plan progress to export.")
                else:
                    writer = csv.DictWriter(buf, fieldnames=["display_name", "plan_name", "total_days", "current_day", "status", "enrolled_at", "completed_at"])
                    writer.writeheader()
                    for r in rows:
                        writer.writerow({k: r.get(k, "") for k in writer.fieldnames})
                    st.download_button(
                        "\U0001f4e5 Download Reading Plan CSV",
                        data=buf.getvalue(),
                        file_name="reading_plan_progress.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                    st.success(f"{len(rows)} records ready.")

            elif exp_type == "Prayer Hours by Member":
                rows = get_prayer_hours_export(exp_start.isoformat(), exp_end.isoformat())
                if not rows:
                    st.info("No prayer entries in that date range.")
                else:
                    writer = csv.DictWriter(buf, fieldnames=["display_name", "role", "total_minutes", "total_hours"])
                    writer.writeheader()
                    for r in rows:
                        writer.writerow({k: r.get(k, "") for k in writer.fieldnames})
                    st.download_button(
                        "\U0001f4e5 Download Prayer Hours CSV",
                        data=buf.getvalue(),
                        file_name=f"prayer_hours_{exp_start}_{exp_end}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                    st.success(f"{len(rows)} members included.")

        except Exception as e:
            st.error(f"Export failed: {e}")
