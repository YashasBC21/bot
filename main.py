import requests
import time
import os
from twilio.rest import Client

# =========================
# 🔐 LOAD ENV VARIABLES
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
YOUR_PHONE = os.getenv("YOUR_PHONE")

# =========================
# 📲 TELEGRAM FUNCTION (DEBUG)
# =========================

def send_telegram(msg):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
        print("Telegram response:", r.text)
    except Exception as e:
        print("Telegram error:", e)

# =========================
# 📱 SMS FUNCTION (DEBUG)
# =========================

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(msg):
    try:
        message = client.messages.create(
            body=msg,
            from_=TWILIO_PHONE,
            to=YOUR_PHONE
        )
        print("SMS sent SID:", message.sid)
    except Exception as e:
        print("SMS error:", e)

# =========================
# 🚀 TEST MODE
# =========================

print("🚀 TEST MODE STARTED")

while True:
    try:
        print("\n--- TEST LOOP ---")

        msg = "🚨 TEST ALERT FROM RCB BOT (RAILWAY)"

        send_telegram(msg)
        send_sms(msg)

        print("✅ TEST ALERT SENT")

    except Exception as e:
        print("Error:", e)

    time.sleep(30)  # avoid spam
