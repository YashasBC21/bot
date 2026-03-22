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

URL = "https://shop.royalchallengers.com"

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

        # 🔥 Detect redirect to Ticketgenie
        if "ticketgenie" in final_url:
            return "REDIRECT"

        # 🔥 Detect ticket-related content
        if "tickets" in text or "book now" in text:
            return "CONTENT"

        return "NONE"

    except Exception as e:
        print("Check error:", e)
        return "ERROR"

# =========================
# 🚀 MAIN LOOP
# =========================

already_alerted = False

print("🚀 RCB Ticket Bot Running...")

while True:
    try:
        status = check_tickets()
        print("Status:", status)

        if status in ["REDIRECT", "CONTENT"] and not already_alerted:
            msg = "🚨 RCB TICKETS MAY BE LIVE!\n\nCheck now:\nhttps://shop.royalchallengers.com"

            send_telegram(msg)
            send_sms("🚨 RCB tickets LIVE! Check now!")

            already_alerted = True

    except Exception as e:
        print("Main loop error:", e)

    time.sleep(10)  # ⚡ 10 sec interval