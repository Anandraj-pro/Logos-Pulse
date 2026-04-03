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

tab_users, tab_create, tab_bulk, tab_analytics = st.tabs([
    "\U0001f465 All Users", "\u2795 Create Account", "\U0001f4e4 Bulk Import", "\U0001f4ca Analytics"
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