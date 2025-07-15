from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from samvidha_scraper import get_attendance_summary  # Your selenium script
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").strip().lower()
    from_number = request.values.get("From", "")
    
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == "attendance":
        msg.body("⏳ Fetching your attendance...")

        # Call Selenium function
        result = get_attendance_summary("your_username", "your_password")
        
        # Send final result
        msg.body(result)
    else:
        msg.body("👋 Hi! Send *Attendance* to check your report.")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
