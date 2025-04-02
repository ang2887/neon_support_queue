# neon_utils.py v1

import os
import requests
from dotenv import load_dotenv
# import logger
from log_config import setup_logger


load_dotenv()
logger = setup_logger("neon_utils")

NEON_API_KEY = os.getenv("NEON_API_KEY")
NEON_PROJECT_ID = os.getenv("NEON_PROJECT_ID")
NEON_API_URL = f"https://console.neon.tech/api/v2/projects/{NEON_PROJECT_ID}"

def fetch_neon_usage():
    logger.info("📡 Fetching Neon usage data...")
    headers = {"Authorization": f"Bearer {NEON_API_KEY}"}
    try:
        response = requests.get(NEON_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        project = data.get("project", {})
        # Correct metric: synthetic_storage_size = live current storage
        storage_bytes = project.get("synthetic_storage_size", 0)
        compute_seconds = project.get("compute_time_seconds", 0)
        storage_gb = storage_bytes / (1024 ** 3)
        compute_cu = compute_seconds / 3600
        logger.info(f"✅Storage: {storage_gb:.2f} GB | Compute: {compute_cu:.2f} CU")
        return storage_gb, compute_cu
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to fetch Neon usage: {e}")
        return None, None
