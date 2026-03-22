import requests
import time
import os
from twilio.rest import Client
from flask import Flask
from threading import Thread

# =========================
# 🔐 LOAD ENV VARIABLES
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
YOUR_PHONE = os.getenv("YOUR_PHONE")

URL = "https://shop.royalchallengers.com"

# =========================
# 🌐 KEEP ALIVE SERVER
# =========================

app = Flask('')

@app.route('/')
def home():
    return "RCB Bot Running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# =========================
# 📲 TELEGRAM FUNCTION
# =========================

def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )
        print("Telegram sent ✅")
    except Exception as e:
        print("Telegram error:", e)

# =========================
# 📱 SMS FUNCTION
# =========================

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(msg):
    try:
        client.messages.create(
            body=msg,
            from_=TWILIO_PHONE,
            to=YOUR_PHONE
        )
        print("SMS sent ✅")
    except Exception as e:
        print("SMS error:", e)

# =========================
# 🔍 CHECK FUNCTION
# =========================

def check_tickets():
    try:
        res = requests.get(URL, allow_redirects=True, timeout=10)

        final_url = res.url.lower()
        text = res.text.lower()

        if "ticketgenie" in final_url:
            return "REDIRECT"

        if "tickets" in text or "book now" in text:
            return "CONTENT"

        return "NONE"

    except Exception as e:
        print("Check error:", e)
        return "ERROR"

# =========================
# 🚀 MAIN BOT
# =========================

keep_alive()   # 🔥 keeps bot awake

already_alerted = False

print("🚀 RCB Ticket Bot Running...")

while True:
    try:
        status = check_tickets()
        print("Status:", status)

        if true:
            msg = "🚨 RCB TICKETS MAY BE LIVE!\n\nCheck now:\nhttps://shop.royalchallengers.com"

            send_telegram(msg)
            send_sms("🚨 RCB tickets LIVE! Check now!")

            already_alerted = True

    except Exception as e:
        print("Main loop error:", e)

    time.sleep(10)
