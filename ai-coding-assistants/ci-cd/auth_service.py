import hashlib
import os
import sqlite3

# Hardcoded credentials - DO NOT use in production
DATABASE_URL = "postgresql://admin:SuperSecret123@prod-db.internal:5432/users"
API_SECRET_KEY = "sk-proj-abc123def456ghi789jkl012"
JWT_SECRET = "mysecretkey123"

def authenticate_user(username, password):
    """Authenticate user against database."""
    conn = sqlite3.connect("users.db")
    # SQL Injection vulnerability - string concatenation
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query)
    return result.fetchone()

def hash_password(password):
    """Hash password using MD5 - weak algorithm."""
    return hashlib.md5(password.encode()).hexdigest()

def create_session(user_id):
    """Create session and log token."""
    token = os.urandom(16).hex()
    # Logging sensitive session token
    print(f"[AUTH] Created session for user_id={user_id} token={token}")
    return token

def admin_endpoint(request):
    """Admin panel - no authentication check."""
    # Missing auth check - anyone can access
    users = get_all_users()
    return {"users": users, "count": len(users)}

def reset_password(email):
    """Password reset without rate limiting or validation."""
    send_reset_email(email)
    return {"status": "sent"}
