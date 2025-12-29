from flask import Flask, request
import requests, os

app = Flask(__name__)

GEMINI_KEY = os.environ.get("GEMINI_KEY")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    user_msg = request.form.get("Body")

    gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_msg}
                ]
            }
        ]
    }

    res = requests.post(gemini_url, json=payload)
    ai_reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]

    requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
        auth=(TWILIO_SID, TWILIO_TOKEN),
        data={
            "From": "whatsapp:+14155238886",
            "To": request.form.get("From"),
            "Body": ai_reply
        }
    )

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
