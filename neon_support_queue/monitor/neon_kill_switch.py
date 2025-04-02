# neon_kill_switch.py v6

import os
from dotenv import load_dotenv
# import logger
from neon_utils import fetch_neon_usage
from email.message import EmailMessage
import smtplib
from log_config import setup_logger


load_dotenv()
logger = setup_logger("neon_kill_switch")

"""
logger.basicConfig(
    level=logger.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logger.FileHandler("neon_kill_switch.log"), logger.StreamHandler()]
)
"""

# Critical kill switch thresholds (close to Neon limit)
CRITICAL_STORAGE_GB = 0.49
CRITICAL_COMPUTE_HOURS = 190

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_email_alert(subject, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("✅ Alert email sent")
    except Exception as e:
        logger.error(f"❌ Failed to send alert email: {e}")

def check_and_kill():
    storage_gb, compute_hours = fetch_neon_usage()
    if storage_gb is None or compute_hours is None:
        logger.warning("⚠️ Skipping due to API failure")
        return
    if storage_gb > CRITICAL_STORAGE_GB or compute_hours > CRITICAL_COMPUTE_HOURS:
        logger.critical("🚨 Usage above limits! Activating kill switch.")
        logger.warning("🛑 Kill switch triggered — alerting for manual intervention...")
        send_email_alert(
            "🛑 Neon Kill Switch Triggered",
            f"Project usage exceeded safe limits.\n\nStorage: {storage_gb:.3f} GB\nCompute: {compute_hours:.2f} hrs\nPlease investigate."
        )
    else:
        logger.info("✅ Resource usage within safe limits")

if __name__ == "__main__":
    check_and_kill()

