"""
Input sanitization for Logos Pulse.
Prevents XSS via unsafe_allow_html=True in Streamlit markdown.
"""

import re
from html import escape


def sanitize_html(text: str) -> str:
    """Escape HTML special characters to prevent XSS injection.
    Preserves newlines (converted to <br/> during rendering).
    """
    if not text:
        return text
    return escape(str(text), quote=True)


def sanitize_dict(data: dict, fields: list[str]) -> dict:
    """Sanitize specific string fields in a dictionary."""
    result = data.copy()
    for field in fields:
        if field in result and isinstance(result[field], str):
            result[field] = sanitize_html(result[field])
    return result


def validate_email(email: str) -> bool:
    """Basic email format validation."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def validate_name(name: str, max_length: int = 50) -> tuple[bool, str]:
    """Validate a name field. Returns (is_valid, error_message)."""
    if not name or not name.strip():
        return False, "This field is required."
    if len(name.strip()) > max_length:
        return False, f"Must be {max_length} characters or less."
    if re.search(r'[<>{}]', name):
        return False, "Invalid characters detected."
    return True, ""


def validate_membership_card(card_id: str) -> tuple[bool, str]:
    """Validate membership card ID format (alphanumeric)."""
    if not card_id or not card_id.strip():
        return True, ""  # Optional field
    if len(card_id.strip()) > 20:
        return False, "Card ID must be 20 characters or less."
    if not re.match(r'^[a-zA-Z0-9]+$', card_id.strip()):
        return False, "Card ID must be alphanumeric (e.g. TKT1694)."
    return True, ""