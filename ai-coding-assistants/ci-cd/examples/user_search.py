"""
User search service - demonstrates SQL injection vulnerability.
This is an intentionally vulnerable example for security review testing.
"""
import sqlite3


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


def search_users(username):
    """Search users by username - VULNERABLE to SQL injection."""
    conn = get_db_connection()
    # String concatenation in SQL query - attacker can inject arbitrary SQL
    query = "SELECT id, username, email, role FROM users WHERE username = '" + username + "'"
    cursor = conn.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


def get_user_orders(user_id, status):
    """Get orders for a user filtered by status - VULNERABLE."""
    conn = get_db_connection()
    # f-string in SQL - allows injection through both parameters
    query = f"SELECT * FROM orders WHERE user_id = {user_id} AND status = '{status}'"
    cursor = conn.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]


def delete_user(user_id):
    """Delete user by ID - VULNERABLE and no authorization check."""
    conn = get_db_connection()
    # No auth check - any caller can delete any user
    # Also vulnerable to injection since user_id is not validated as integer
    conn.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    conn.close()
    return {"deleted": True}


def update_user_role(username, new_role):
    """Update user role - VULNERABLE to injection in UPDATE statement."""
    conn = get_db_connection()
    query = "UPDATE users SET role = '%s' WHERE username = '%s'" % (new_role, username)
    conn.execute(query)
    conn.commit()
    conn.close()
    return {"updated": True}
