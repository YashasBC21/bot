import requests
import time
import os
from twilio.rest import Client

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
YOUR_PHONE = os.getenv("YOUR_PHONE")

URL = "https://shop.royalchallengers.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ================== TELEGRAM ==================
def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
        print("Telegram sent")
    except Exception as e:
        print("Telegram error:", e)

# ================== SMS ==================
client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(msg):
    try:
        client.messages.create(
            body=msg,
            from_=TWILIO_PHONE,
            to=YOUR_PHONE
        )
        print("SMS sent")
    except Exception as e:
        print("SMS error:", e)

# ================== CHECK FUNCTION ==================
def check_tickets():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10)

        final_url = res.url.lower()
        text = res.text.lower()

        # Debug (optional)
        if "buy tickets" in text:
            print("DEBUG: 'buy tickets' found")

        if "/ticket" in final_url or "ticket" in text:

            if (
                "buy tickets" in text and
                "href" in text and
                "disabled" not in text and
                "sold out" not in text and
                "coming soon" not in text and
                "notify me" not in text
            ):
                return "LIVE"

            return "PAGE_ONLY"

        return "CLOSED"

    except Exception as e:
        print("Check error:", e)
        return "ERROR"

# ================== MAIN LOOP ==================
already_alerted = False
last_status = None
confirm_count = 0

print("RCB Ticket Bot Running...")

while True:
    try:
        status = check_tickets()
        print("Status:", status)

        if status == "LIVE":
            if last_status == "LIVE":
                confirm_count += 1
            else:
                confirm_count = 1

            # Require 2 confirmations
            if confirm_count >= 2 and not already_alerted:
                msg = "RCB tickets are LIVE. Check now: https://shop.royalchallengers.com"
                send_telegram(msg)
                send_sms("RCB tickets LIVE. Check now.")
                already_alerted = True

        else:
            confirm_count = 0

            # Reset only when fully closed
            if status == "CLOSED":
                already_alerted = False

        last_status = status

    except Exception as e:
        print("Main loop error:", e)

    time.sleep(30)
