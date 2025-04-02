# neon_post_data_test.py 

import os
import psycopg2
from dotenv import load_dotenv
from data_generator import *

load_dotenv()

USE_NEON = os.getenv("USE_NEON", "0") == "1"
DATABASE_URL = os.getenv("NEON_DB_URL") if USE_NEON else os.getenv("SUPABASE_DB_URL")

# Generate the data using the support_queue_data_generator function with the params
params = {
    'NUM_COMPANIES':  50,
    'NUM_USERS': 1000,
    'NUM_SUPPORT_STAFF': 50,
    'NUM_TICKETS': 5000, 
    'TICKET_CATEGORIES': ['Technical', 'Billing', 'Account', 'General Inquiry'],
    'mean': 2,
    'sigma': 1,
    'user_probs_limit': 100
}

tables = support_queue_data_generator(params)

# Print first few rows of each table instead of inserting data
print("✅ Running in TEST MODE: No database connection\n")

for table_name, df in tables.items():
    print(f"🔹 Table: {table_name}")
    print(df.head(3))  # Print only first 3 rows
    print("\n" + "-"*50 + "\n")