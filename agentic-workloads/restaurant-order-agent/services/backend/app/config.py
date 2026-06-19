import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
RESTAURANT_API_BASE = os.getenv("RESTAURANT_API_BASE", "")
RESTAURANT_API_KEY = os.getenv("RESTAURANT_API_KEY", "")
SNS_SENDER_ID = os.getenv("SNS_SENDER_ID", "TastyApp")
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Comma-separated list of allowed CORS origins. Defaults to local dev ports.
CORS_ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:3001,http://localhost:5173,http://localhost:5174",
    ).split(",")
    if o.strip()
]

# Validate critical configuration at startup
if not JWT_SECRET:
    logger.critical("JWT_SECRET is not set. Refusing to start with empty secret.")
    sys.exit(1)

if not RESTAURANT_API_BASE:
    logger.warning("RESTAURANT_API_BASE is not set — API calls will fail.")
