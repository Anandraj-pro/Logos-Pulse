"""SMTP email sender for Logos Pulse weekly digests.

Requires [email] section in .streamlit/secrets.toml:
    [email]
    smtp_host   = "smtp.gmail.com"
    smtp_port   = 587
    smtp_user   = "your@gmail.com"
    smtp_password = "your-app-password"
    from_name   = "Logos Pulse"
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st


def _cfg() -> dict | None:
    try:
        return dict(st.secrets["email"])
    except Exception:
        return None


def is_configured() -> bool:
    cfg = _cfg()
    return bool(cfg and cfg.get("smtp_host") and cfg.get("smtp_user") and cfg.get("smtp_password"))


def send_email(to_address: str, subject: str, body: str) -> dict:
    """Send a plain-text email. Returns {"success": True} or {"success": False, "error": ...}."""
    cfg = _cfg()
    if not cfg:
        return {"success": False, "error": "Email not configured in secrets.toml"}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{cfg.get('from_name', 'Logos Pulse')} <{cfg['smtp_user']}>"
        msg["To"]      = to_address
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(cfg["smtp_host"], int(cfg.get("smtp_port", 587))) as server:
            server.ehlo()
            server.starttls()
            server.login(cfg["smtp_user"], cfg["smtp_password"])
            server.sendmail(cfg["smtp_user"], to_address, msg.as_string())

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_bulk(recipients: list[dict]) -> dict:
    """Send digests to multiple recipients.
    Each item: {"to": email, "subject": str, "body": str}
    Returns {"sent": N, "failed": [...errors]}
    """
    sent, failed = 0, []
    for r in recipients:
        result = send_email(r["to"], r["subject"], r["body"])
        if result["success"]:
            sent += 1
        else:
            failed.append({"email": r["to"], "error": result["error"]})
    return {"sent": sent, "failed": failed}
