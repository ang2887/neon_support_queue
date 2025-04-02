# neon_monitor.py v6

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import schedule
import time
from neon_utils import fetch_neon_usage
from log_config import setup_logger


load_dotenv()
logger = setup_logger("neon_monitor")

"""
logger.basicConfig(
    level=logger.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logger.FileHandler("neon_monitor.log"), logger.StreamHandler()]
)
"""
# Soft threshold for warning (email alert only) (below Neon free-tier limits)
THRESHOLD_STORAGE_GB = 0.45
THRESHOLD_COMPUTE_HOURS = 180

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
        logger.error(f"❌ Email sending failed: {e}")

def monitor_usage():
    storage_gb, compute_hours = fetch_neon_usage()
    logger.info(f"✅Storage: {storage_gb:.2f} GB | Compute: {compute_hours:.2f} CU")

    if storage_gb is None or compute_hours is None:
        logger.warning("⚠️ Skipping due to API issues")
        return
    alert_triggered = False
    alert_message = "📢 Neon Usage Alert 🚨\n\n"
    if storage_gb > THRESHOLD_STORAGE_GB:
        alert_message += f"❗ Storage high: {storage_gb:.3f} GB (Threshold: {THRESHOLD_STORAGE_GB})\n"
        alert_triggered = True
    if compute_hours > THRESHOLD_COMPUTE_HOURS:
        alert_message += f"❗ Compute high: {compute_hours:.2f} hrs (Threshold: {THRESHOLD_COMPUTE_HOURS})\n"
        alert_triggered = True
    if alert_triggered:
        logger.warning(alert_message)
        send_email_alert("🚨 Neon DB Usage Alert", alert_message)
    else:
        logger.info("✅ Usage within safe limits")

# Scheduled daily + immediate first check
schedule.every().day.at("07:00").do(monitor_usage)
monitor_usage()
logger.info("⏳ Monitoring script running...")

# while True:  # Optional background loop
#     schedule.run_pending()
#     time.sleep(60)