import os
from dotenv import load_dotenv

class Config:
    _instance = None  # stores the one instance

    def __new__(cls):
        if cls._instance is None: # only create if it doesn't exist yet
            load_dotenv()
            cls._instance = super().__new__(cls)
            cls._instance.BASE_URL = os.getenv("BASE_URL", "https://api-bug-buddy.lovable.app")
            cls._instance.TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL")
            cls._instance.TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")
            cls._instance.TEST_FIRST_NAME = os.getenv("TEST_FIRST_NAME")
            cls._instance.TEST_LAST_NAME = os.getenv("TEST_LAST_NAME")
        return cls._instance

config = Config()