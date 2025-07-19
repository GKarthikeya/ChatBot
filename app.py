from flask import Flask, request, jsonify
from samvidha_scraper import login_and_scrape  # you should define this

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Samvidha Bot is live!"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    result = login_and_scrape(username, password)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run()
