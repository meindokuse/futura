import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_KEY = os.environ.get("SECRET_KEY")
REFRESH_SECRET_KEY = os.environ.get("REFRESH_SECRET_KEY")

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME", "Currency Alert System")
MAIL_STARTTLS = os.environ.get("MAIL_STARTTLS", "True") == "True"
MAIL_SSL_TLS = os.environ.get("MAIL_SSL_TLS", "False") == "True"
USE_CREDENTIALS = os.environ.get("USE_CREDENTIALS", "True") == "True"
VALIDATE_CERTS = os.environ.get("VALIDATE_CERTS", "True") == "True"

VERIFICATION_CODE_TTL = 600

REDIS_URL = os.environ.get("REDIS_URL")
BOT_URL = os.environ.get("BOT_URL")
