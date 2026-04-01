"""
Authentication module for Logos Pulse.
Handles login, signup, session management, and auth guards.
"""

import streamlit as st
from modules.supabase_client import get_supabase_client, get_admin_client


# Role-specific default passwords
DEFAULT_PASSWORDS = {
    "admin": "Raju@002",
    "bishop": "Bishop@123",
    "pastor": "Pastor@123",
    "prayer_warrior": "Open@123",
}


def sign_in(email: str, password: str) -> dict:
    """Sign in a user. Returns dict with 'success', 'user', 'error'."""
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        user = response.user
        session = response.session

        # Fetch profile for role and metadata
        admin = get_admin_client()
        profile = admin.table("user_profiles") \
            .select("*") \
            .eq("user_id", user.id) \
            .single() \
            .execute()

        profile_data = profile.data

        # Store in session state
        st.session_state["authenticated"] = True
        st.session_state["user_id"] = user.id
        st.session_state["user_email"] = user.email
        st.session_state["access_token"] = session.access_token
        st.session_state["refresh_token"] = session.refresh_token
        st.session_state["role"] = profile_data["role"]
        st.session_state["must_change_password"] = profile_data.get("must_change_password", False)
        st.session_state["preferred_name"] = (
            user.user_metadata.get("preferred_name")
            or user.user_metadata.get("first_name")
            or email.split("@")[0]
        )

        return {"success": True, "user": user, "profile": profile_data}

    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            return {"success": False, "error": "Invalid email or password."}
        return {"success": False, "error": f"Login failed: {error_msg}"}


def sign_up(email: str, password: str, first_name: str, last_name: str,
            preferred_name: str, pastor_id: str, prayer_benchmark: int = 60,
            membership_card_id: str = None) -> dict:
    """Register a new Prayer Warrior. Returns dict with 'success', 'error'."""
    try:
        admin = get_admin_client()

        # Create auth user via admin API
        response = admin.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {
                "first_name": first_name,
                "last_name": last_name,
                "preferred_name": preferred_name or first_name,
            },
        })

        user = response.user

        # Create user profile
        admin.table("user_profiles").insert({
            "user_id": user.id,
            "role": "prayer_warrior",
            "pastor_id": pastor_id,
            "prayer_benchmark_min": prayer_benchmark,
            "membership_card_id": membership_card_id or None,
            "must_change_password": True,
        }).execute()

        return {"success": True, "user_id": user.id}

    except Exception as e:
        error_msg = str(e)
        if "already been registered" in error_msg or "duplicate" in error_msg.lower():
            return {"success": False, "error": "An account with this email already exists."}
        return {"success": False, "error": f"Registration failed: {error_msg}"}


def sign_out():
    """Sign out the current user and clear session."""
    try:
        client = get_supabase_client()
        client.auth.sign_out()
    except Exception:
        pass

    keys_to_clear = [
        "authenticated", "user_id", "user_email", "access_token",
        "refresh_token", "role", "must_change_password", "preferred_name",
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)


def change_password(new_password: str) -> dict:
    """Change the current user's password."""
    try:
        client = get_supabase_client()

        # Set auth header for the current user
        token = st.session_state.get("access_token")
        refresh = st.session_state.get("refresh_token")

        if not token or not refresh:
            return {"success": False, "error": "Session expired. Please log in again."}

        try:
            client.auth.set_session(token, refresh)
        except Exception:
            # Try refreshing the session first
            try:
                response = client.auth.refresh_session(refresh)
                if response and response.session:
                    st.session_state["access_token"] = response.session.access_token
                    st.session_state["refresh_token"] = response.session.refresh_token
                    client.auth.set_session(
                        response.session.access_token,
                        response.session.refresh_token,
                    )
                else:
                    return {"success": False, "error": "Session expired. Please log in again."}
            except Exception:
                return {"success": False, "error": "Session expired. Please log in again."}

        client.auth.update_user({"password": new_password})

        # Clear the must_change_password flag
        admin = get_admin_client()
        admin.table("user_profiles") \
            .update({"must_change_password": False}) \
            .eq("user_id", st.session_state["user_id"]) \
            .execute()

        st.session_state["must_change_password"] = False
        return {"success": True}

    except Exception as e:
        error_msg = str(e)
        if "same_password" in error_msg.lower() or "different" in error_msg.lower():
            return {"success": False, "error": "New password must be different from the current one."}
        if "weak" in error_msg.lower() or "short" in error_msg.lower():
            return {"success": False, "error": "Password is too weak. Use at least 8 characters with a mix of letters and numbers."}
        return {"success": False, "error": f"Password change failed: {error_msg}"}


def request_password_reset(email: str) -> dict:
    """Send a password reset email via Supabase."""
    try:
        client = get_supabase_client()
        client.auth.reset_password_email(email)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def is_authenticated() -> bool:
    """Check if the current session is authenticated."""
    return st.session_state.get("authenticated", False)


def get_current_role() -> str:
    """Get the current user's role."""
    return st.session_state.get("role", "")


def get_current_user_id() -> str:
    """Get the current user's ID."""
    return st.session_state.get("user_id", "")


def require_login():
    """Auth guard — stops page execution if not logged in."""
    if not is_authenticated():
        st.warning("Please log in to access this page.")
        st.stop()


def require_role(allowed_roles: list):
    """Role guard — stops page execution if user doesn't have required role."""
    require_login()
    if st.session_state.get("must_change_password"):
        st.warning("You must change your password before using the app.")
        st.switch_page("views/Change_Password.py")
    role = get_current_role()
    if role not in allowed_roles:
        st.error("You don't have permission to access this page.")
        st.stop()


def require_password_changed():
    """Guard — redirects to password change if still using default."""
    require_login()
    if st.session_state.get("must_change_password"):
        st.switch_page("views/Change_Password.py")