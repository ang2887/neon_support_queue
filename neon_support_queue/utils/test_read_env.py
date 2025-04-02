#test_read_env.py 

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("EMAIL_SENDER:", os.getenv("EMAIL_SENDER"))
print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))  # Just for testing, remove later!
print("EMAIL_RECEIVER:", os.getenv("EMAIL_RECEIVER"))