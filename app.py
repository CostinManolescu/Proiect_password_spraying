from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

users_db = {
    "user1": generate_password_hash("StrongPass123"),
    "user2": generate_password_hash("Secure!456"),
    "user3": generate_password_hash("Welcome123"),
    "user4": generate_password_hash("Security10"),
}

login_attempts = defaultdict(list)
ip_attempts = defaultdict(list)

PASSWORD_RATE_LIMIT = 3
RATE_LIMIT_TIMEFRAME = timedelta(minutes=1)
IP_RATE_LIMIT = 50

@app.route("/login", methods=["POST"])
def login():
    ip = request.remote_addr
    now = datetime.now()
    username = request.form.get("username")
    password = request.form.get("password")

    ip_attempts[ip] = [t for t in ip_attempts[ip] if now - t < RATE_LIMIT_TIMEFRAME]
    if len(ip_attempts[ip]) >= IP_RATE_LIMIT:
        return jsonify({"error": "Too many requests from this IP. Try again later."}), 429

    login_attempts[password] = [t for t in login_attempts[password] if now - t < RATE_LIMIT_TIMEFRAME]
    if len(login_attempts[password]) >= PASSWORD_RATE_LIMIT:
        return jsonify({"error": "This password has been temporarily blocked due to excessive use."}), 429

    if username in users_db and check_password_hash(users_db[username], password):
        return jsonify({"message": "Login successful!"}), 200

    login_attempts[password].append(now)
    ip_attempts[ip].append(now)
    
    return jsonify({"error": "Invalid username or password."}), 401

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users_db:
        return jsonify({"error": "Username already exists."}), 400

    users_db[username] = generate_password_hash(password)
    return jsonify({"message": "User registered successfully!"}), 201

@app.route("/delete_user", methods=["DELETE"])
def delete_user():
    username = request.form.get("username")

    if username not in users_db:
        return jsonify({"error": "User not found."}), 404

    del users_db[username]
    return jsonify({"message": f"User '{username}' has been deleted."}), 200

if __name__ == "__main__":
    app.run(debug=True)

