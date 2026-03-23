import requests
import time
import os
from twilio.rest import Client

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
YOUR_PHONE = os.getenv("YOUR_PHONE")

URL = "https://shop.royalchallengers.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

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

def check_tickets():
    try:
        res = requests.get(URL, headers=HEADERS, allow_redirects=True, timeout=10)
        final_url = res.url.lower()
        text = res.text.lower()

        if "/ticket" in final_url:
            if "buy tickets" in text or "select seats" in text or "book now" in text:
                return "LIVE"
            return "PAGE_ONLY"

        return "CLOSED"

    except Exception as e:
        print("Check error:", e)
        return "ERROR"

already_alerted = False

print("RCB Ticket Bot Running...")

while True:
    try:
        status = check_tickets()
        print("Status:", status)

        if status == "LIVE" and not already_alerted:
            msg = "RCB tickets may be live. Check now: https://shop.royalchallengers.com"
            send_telegram(msg)
            send_sms("RCB tickets live. Check now.")
            already_alerted = True

        elif status != "LIVE":
            already_alerted = False

    except Exception as e:
        print("Main loop error:", e)

    time.sleep(10)