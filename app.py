from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from samvidha_scraper import get_attendance_summary
from twilio.rest import Client
from threading import Thread
import os

app = Flask(__name__)

# Per‑user finite‑state machine stored in memory
user_states = {}           # {whatsapp_number: {"stage": str, ...}}

# Twilio REST client for proactive messages
client = Client(os.environ["TWILIO_ACCOUNT_SID"],
                os.environ["TWILIO_AUTH_TOKEN"])
FROM_WHATSAPP = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

def run_scraper_and_reply(to_number: str, username: str, password: str):
    """Background job: scrape and send result via REST API."""
    result = get_attendance_summary(username, password)
    client.messages.create(
        from_=FROM_WHATSAPP,
        to=to_number,
        body=result
    )

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    body = request.values.get("Body", "").strip()
    from_num = request.values.get("From")
    state = user_states.get(from_num, {"stage": None})

    twiml = MessagingResponse()
    msg = twiml.message()

    if body.lower() == "attendance":
        user_states[from_num] = {"stage": "await_username"}
        msg.body("👤 Enter your *Samvidha* username:")
    elif state["stage"] == "await_username":
        state["username"] = body
        state["stage"] = "await_password"
        msg.body("🔒 Enter your *Samvidha* password:")
    elif state["stage"] == "await_password":
        username, password = state["username"], body
        msg.body("⏳ Fetching your attendance… you’ll receive it shortly.")
        # fire‑and‑forget background job
        Thread(target=run_scraper_and_reply,
               args=(from_num, username, password),
               daemon=True).start()
        user_states.pop(from_num, None)  # clear session
    else:
        msg.body("👋 Send *Attendance* to begin.")

    return str(twiml)

if __name__ == "__main__":
    app.run(port=5000)
