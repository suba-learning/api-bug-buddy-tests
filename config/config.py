import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api-bug-buddy.lovable.app")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
TEST_FIRST_NAME = os.getenv("TEST_FIRST_NAME")
TEST_LAST_NAME = os.getenv("TEST_LAST_NAME")