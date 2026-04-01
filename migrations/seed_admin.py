"""
One-time script to seed the Admin account.
Run locally after executing 001_schema.sql in Supabase SQL Editor.

Usage:
    cd /Users/bhargavigunnam/PycharmProjects/Daily_Assignment
    python migrations/seed_admin.py admin@logospulse.com "Admin" "User"
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Must set up streamlit secrets before importing modules
# This script reads from .streamlit/secrets.toml via toml
import toml

secrets_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".streamlit", "secrets.toml"
)
secrets = toml.load(secrets_path)

from supabase import create_client

def seed_admin(email: str, first_name: str, last_name: str):
    url = secrets["supabase"]["url"]
    service_key = secrets["supabase"]["service_role_key"]

    admin_client = create_client(url, service_key)

    print(f"Creating admin account: {email}")

    # Create auth user
    response = admin_client.auth.admin.create_user({
        "email": email,
        "password": "Raju@002",
        "email_confirm": True,
        "user_metadata": {
            "first_name": first_name,
            "last_name": last_name,
            "preferred_name": first_name,
        },
    })

    user = response.user
    print(f"Auth user created: {user.id}")

    # Create profile
    admin_client.table("user_profiles").insert({
        "user_id": user.id,
        "role": "admin",
        "must_change_password": True,
        "prayer_benchmark_min": 60,
    }).execute()

    print(f"Admin profile created.")
    print(f"\nAdmin account ready:")
    print(f"  Email:    {email}")
    print(f"  Password: Raju@002 (must change on first login)")
    print(f"  Role:     admin")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python migrations/seed_admin.py <email> <first_name> <last_name>")
        print("Example: python migrations/seed_admin.py admin@logospulse.com Admin User")
        sys.exit(1)

    seed_admin(sys.argv[1], sys.argv[2], sys.argv[3])