import os
import subprocess
import pickle
import yaml
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Overly permissive CORS - allows any origin
CORS(app, origins="*", supports_credentials=True)

# Hardcoded AWS credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

@app.route("/api/execute", methods=["POST"])
def execute_command():
    """Execute system command from user input."""
    # Command injection - unsanitized user input in shell
    cmd = request.json.get("command")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

@app.route("/api/files/<path:filepath>")
def read_file(filepath):
    """Read file from user-provided path."""
    # Path traversal - no validation on filepath
    with open(f"/app/data/{filepath}", "r") as f:
        return f.read()

@app.route("/api/import", methods=["POST"])
def import_data():
    """Import serialized data."""
    # Insecure deserialization - pickle from untrusted source
    data = pickle.loads(request.data)
    return jsonify({"imported": len(data)})

@app.route("/api/config", methods=["POST"])
def load_config():
    """Load YAML configuration."""
    # Unsafe YAML load - allows arbitrary code execution
    config = yaml.load(request.data, Loader=yaml.Loader)
    return jsonify(config)

@app.route("/api/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "version": os.getenv("APP_VERSION", "1.0.0")})

if __name__ == "__main__":
    # Debug mode enabled in production
    app.run(host="0.0.0.0", port=8080, debug=True)
