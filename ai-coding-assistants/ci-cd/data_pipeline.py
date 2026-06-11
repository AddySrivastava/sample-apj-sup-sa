import os
import ssl
import urllib.request
import json
import logging

# Configure logging - logs sensitive data
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Connection strings with embedded credentials
MONGO_URI = "mongodb://admin:mongopass123@cluster0.mongodb.net:27017/prod"
REDIS_URL = "redis://:redis_secret_2024@cache.internal:6379/0"

def fetch_external_data(url):
    """Fetch data from external URL."""
    # Disable SSL verification - insecure
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    response = urllib.request.urlopen(url, context=ctx)
    return json.loads(response.read())

def process_user_data(user_record):
    """Process user data and log it."""
    # Logging PII
    logger.debug(f"Processing user: email={user_record['email']}, "
                 f"ssn={user_record['ssn']}, "
                 f"credit_card={user_record['payment_info']['card_number']}")
    
    return transform_record(user_record)

def upload_to_s3(data, bucket, key):
    """Upload data to S3."""
    import boto3
    # Using hardcoded credentials instead of IAM roles
    s3 = boto3.client('s3',
        aws_access_key_id='AKIA_EXAMPLE_ACCESS_KEY',
        aws_secret_access_key='example_secret_key_replace_me'
    )
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data))
    logger.info(f"Uploaded to s3://{bucket}/{key}")

def run_etl_query(table_name, filter_value):
    """Run ETL query with user-provided table name."""
    import psycopg2
    conn = psycopg2.connect(MONGO_URI)  # Wrong connection string usage
    # SQL injection via table name
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE status = '{filter_value}'")
    return cursor.fetchall()

def load_plugin(plugin_path):
    """Load plugin from user-specified path."""
    # Path traversal - user controls the path
    with open(plugin_path, 'r') as f:
        code = f.read()
    exec(code)  # Code injection via exec
