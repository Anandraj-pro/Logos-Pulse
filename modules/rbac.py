"""
Role-Based Access Control helpers for Logos Pulse.
Admin operations for creating/managing accounts across the role hierarchy.
"""

from modules.supabase_client import get_admin_client
from modules.auth import DEFAULT_PASSWORDS


def create_account(email: str, first_name: str, last_name: str, role: str,
                   created_by: str, pastor_id: str = None, bishop_id: str = None,
                   prayer_benchmark: int = 60, membership_card_id: str = None,
                   region_or_group: str = "") -> dict:
    """Create a new account for any role. Must be called by authorized user.
    Returns dict with 'success', 'user_id', 'error'.
    """
    if role not in DEFAULT_PASSWORDS:
        return {"success": False, "error": f"Invalid role: {role}"}

    try:
        admin = get_admin_client()

        # Create auth user with role-specific default password
        response = admin.auth.admin.create_user({
            "email": email,
            "password": DEFAULT_PASSWORDS[role],
            "email_confirm": True,
            "user_metadata": {
                "first_name": first_name,
                "last_name": last_name,
                "preferred_name": first_name,
            },
        })

        user = response.user

        # Build profile row
        profile = {
            "user_id": user.id,
            "role": role,
            "created_by": created_by,
            "prayer_benchmark_min": prayer_benchmark,
            "must_change_password": True,
            "membership_card_id": membership_card_id or None,
            "region_or_group": region_or_group,
        }

        if role == "prayer_warrior" and pastor_id:
            profile["pastor_id"] = pastor_id
        if role == "pastor" and bishop_id:
            profile["bishop_id"] = bishop_id

        admin.table("user_profiles").insert(profile).execute()

        # Auto-seed default data for prayer warriors
        if role == "prayer_warrior":
            try:
                from modules.seed import seed_user_data
                from modules import db as _db
                seed_user_data(user.id, first_name, prayer_benchmark)
                _db.seed_new_believer_plan(user.id)
            except Exception:
                pass  # Non-critical — user can still use the app without seed data

        try:
            from modules import db as _db
            _db.log_audit("user.created", target_type="user", target_id=user.id,
                          details={"email": email, "role": role})
        except Exception:
            pass

        return {"success": True, "user_id": user.id}

    except Exception as e:
        error_msg = str(e)
        if "already been registered" in error_msg or "duplicate" in error_msg.lower():
            return {"success": False, "error": "An account with this email already exists."}
        return {"success": False, "error": f"Account creation failed: {error_msg}"}


def get_users_by_role(role: str) -> list:
    """Get all users with a specific role. Uses admin client (bypasses RLS)."""
    admin = get_admin_client()
    result = admin.table("user_profiles") \
        .select("*, auth_user:user_id(email, raw_user_meta_data)") \
        .eq("role", role) \
        .execute()
    return result.data or []


def get_pastors_list() -> list:
    """Get list of pastors for dropdown (id + display name).
    Returns list of dicts with 'user_id' and 'display_name'.
    """
    admin = get_admin_client()
    result = admin.table("user_profiles") \
        .select("user_id") \
        .eq("role", "pastor") \
        .execute()

    pastors = []
    if result.data:
        for row in result.data:
            user_resp = admin.auth.admin.get_user_by_id(row["user_id"])
            user = user_resp.user
            meta = user.user_metadata or {}
            name = meta.get("preferred_name") or meta.get("first_name") or user.email
            pastors.append({
                "user_id": row["user_id"],
                "display_name": name,
                "email": user.email,
            })
    return pastors


def get_bishops_list() -> list:
    """Get list of bishops for dropdown."""
    admin = get_admin_client()
    result = admin.table("user_profiles") \
        .select("user_id") \
        .eq("role", "bishop") \
        .execute()

    bishops = []
    if result.data:
        for row in result.data:
            user_resp = admin.auth.admin.get_user_by_id(row["user_id"])
            user = user_resp.user
            meta = user.user_metadata or {}
            name = meta.get("preferred_name") or meta.get("first_name") or user.email
            bishops.append({
                "user_id": row["user_id"],
                "display_name": name,
                "email": user.email,
            })
    return bishops


def get_members_for_pastor(pastor_id: str) -> list:
    """Get all prayer warriors assigned to a specific pastor."""
    admin = get_admin_client()
    result = admin.table("user_profiles") \
        .select("user_id, membership_card_id, prayer_benchmark_min") \
        .eq("pastor_id", pastor_id) \
        .eq("role", "prayer_warrior") \
        .execute()

    members = []
    if result.data:
        for row in result.data:
            user_resp = admin.auth.admin.get_user_by_id(row["user_id"])
            user = user_resp.user
            meta = user.user_metadata or {}
            name = meta.get("preferred_name") or meta.get("first_name") or user.email
            members.append({
                "user_id": row["user_id"],
                "display_name": name,
                "email": user.email,
                "membership_card_id": row.get("membership_card_id"),
                "prayer_benchmark_min": row.get("prayer_benchmark_min", 60),
            })
    return members


def get_pastors_for_bishop(bishop_id: str) -> list:
    """Get all pastors assigned to a specific bishop."""
    admin = get_admin_client()
    result = admin.table("user_profiles") \
        .select("user_id, region_or_group") \
        .eq("bishop_id", bishop_id) \
        .eq("role", "pastor") \
        .execute()

    pastors = []
    if result.data:
        for row in result.data:
            user_resp = admin.auth.admin.get_user_by_id(row["user_id"])
            user = user_resp.user
            meta = user.user_metadata or {}
            name = meta.get("preferred_name") or meta.get("first_name") or user.email
            # Count members under this pastor
            members_count = admin.table("user_profiles") \
                .select("id", count="exact") \
                .eq("pastor_id", row["user_id"]) \
                .execute()
            pastors.append({
                "user_id": row["user_id"],
                "display_name": name,
                "email": user.email,
                "region_or_group": row.get("region_or_group", ""),
                "members_count": members_count.count or 0,
            })
    return pastors


def reset_user_password(user_id: str, role: str) -> dict:
    """Reset a user's password to the role-specific default."""
    try:
        admin = get_admin_client()
        default_pw = DEFAULT_PASSWORDS.get(role, "Open@123")

        admin.auth.admin.update_user_by_id(user_id, {
            "password": default_pw,
        })

        admin.table("user_profiles") \
            .update({"must_change_password": True}) \
            .eq("user_id", user_id) \
            .execute()

        try:
            from modules import db as _db
            _db.log_audit("user.password_reset", target_type="user", target_id=user_id,
                          details={"role": role})
        except Exception:
            pass

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_account(user_id: str) -> dict:
    """Delete a user account (admin only). Cascades via FK."""
    try:
        admin = get_admin_client()
        admin.auth.admin.delete_user(user_id)
        try:
            from modules import db as _db
            _db.log_audit("user.deleted", target_type="user", target_id=user_id)
        except Exception:
            pass
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}