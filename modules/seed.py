"""
Seed data for new user registrations.
Pushes default prayer categories, prayers, and settings.
"""

from modules.supabase_client import get_admin_client


DEFAULT_PRAYER_CATEGORIES = [
    {"name": "Personal", "icon": "\U0001f64f", "color": "#5B4FC4"},
    {"name": "Finances", "icon": "\U0001f4b0", "color": "#3A8F5C"},
    {"name": "Spouse", "icon": "\u2764\ufe0f", "color": "#C44B5B"},
    {"name": "Career", "icon": "\U0001f4bc", "color": "#D4853A"},
]

DEFAULT_PRAYERS = {
    "Personal": {
        "title": "Daily Spiritual Growth",
        "prayer_text": "Dear Lord, I ask for Your guidance and wisdom in my daily walk with You. Help me to grow in faith, love, and obedience.",
        "confessions": "I confess that God is my source of strength.\nI confess that I am a new creation in Christ.\nI confess that the Holy Spirit guides my steps.",
        "declarations": "I declare that this is a season of growth and transformation.\nI declare that I will walk in the fullness of God's plan for my life.\nI declare that no weapon formed against me shall prosper.",
    },
}

DEFAULT_SETTINGS = {
    "omit_empty_sermon": "false",
}


def seed_user_data(user_id: str, preferred_name: str, prayer_benchmark: int = 60):
    """Push default data for a newly registered user."""
    admin = get_admin_client()

    # 1. Seed settings
    settings_rows = [
        {"user_id": user_id, "key": "greeting_name", "value": preferred_name},
        {"user_id": user_id, "key": "default_prayer_minutes", "value": str(prayer_benchmark)},
    ]
    for key, value in DEFAULT_SETTINGS.items():
        settings_rows.append({"user_id": user_id, "key": key, "value": value})

    admin.table("app_settings").insert(settings_rows).execute()

    # 2. Seed prayer categories
    category_ids = {}
    for cat in DEFAULT_PRAYER_CATEGORIES:
        result = admin.table("prayer_categories").insert({
            "user_id": user_id,
            "name": cat["name"],
            "icon": cat["icon"],
            "color": cat["color"],
        }).execute()
        if result.data:
            category_ids[cat["name"]] = result.data[0]["id"]

    # 3. Seed default prayers
    for cat_name, prayer_data in DEFAULT_PRAYERS.items():
        cat_id = category_ids.get(cat_name)
        if cat_id:
            admin.table("prayer_entries").insert({
                "user_id": user_id,
                "category_id": cat_id,
                "title": prayer_data["title"],
                "prayer_text": prayer_data["prayer_text"],
                "confessions": prayer_data["confessions"],
                "declarations": prayer_data["declarations"],
                "status": "ongoing",
            }).execute()