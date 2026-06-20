"""
File processing service - demonstrates command injection and path traversal.
This is an intentionally vulnerable example for security review testing.
"""
import os
import subprocess
import pickle
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


@app.route("/api/convert", methods=["POST"])
def convert_file():
    """Convert file format using system command - VULNERABLE to command injection."""
    input_file = request.json.get("input_file")
    output_format = request.json.get("format")
    # User input directly interpolated into shell command
    cmd = f"convert {input_file} -format {output_format} output.{output_format}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({"status": "done", "output": result.stdout})


@app.route("/api/logs", methods=["GET"])
def get_logs():
    """Retrieve log file - VULNERABLE to path traversal."""
    log_name = request.args.get("name", "app.log")
    # No validation - attacker can use ../../etc/passwd
    log_path = os.path.join("/var/logs", log_name)
    with open(log_path, "r") as f:
        content = f.read()
    return jsonify({"log": content})


@app.route("/api/download/<path:filename>")
def download_file(filename):
    """Download file - VULNERABLE to path traversal."""
    # User-controlled path with no sanitization
    file_path = f"/app/uploads/{filename}"
    if os.path.exists(file_path):
        return send_file(file_path)
    return jsonify({"error": "not found"}), 404


@app.route("/api/process", methods=["POST"])
def process_data():
    """Process uploaded data - VULNERABLE to insecure deserialization."""
    # Pickle deserialization of untrusted input allows arbitrary code execution
    data = pickle.loads(request.data)
    return jsonify({"processed": len(data), "type": str(type(data))})


@app.route("/api/ping", methods=["POST"])
def ping_host():
    """Ping a host - VULNERABLE to command injection."""
    host = request.json.get("host")
    # Unsanitized input passed to os.system
    exit_code = os.system(f"ping -c 3 {host}")
    return jsonify({"reachable": exit_code == 0})


@app.route("/api/backup", methods=["POST"])
def create_backup():
    """Create backup - VULNERABLE to command injection via filename."""
    filename = request.json.get("filename")
    # Attacker can inject: filename="; rm -rf / #"
    os.system(f"tar -czf /backups/{filename}.tar.gz /app/data")
    return jsonify({"status": "backup created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
