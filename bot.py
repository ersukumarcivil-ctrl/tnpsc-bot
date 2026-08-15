import os
import requests
from bs4 import BeautifulSoup

# GitHub Secrets-ல் இருந்து ரகசியத் தகவல்களை எடுப்பது
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# TNPSC அறிவிப்புப் பக்கம்
URL = "https://www.tnpsc.gov.in/english/notification.aspx"

def get_latest_notifications():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        notifications = []
        for a_tag in soup.find_all('a', href=True):
            if 'notification' in a_tag['href'].lower() or '.pdf' in a_tag['href'].lower():
                text = a_tag.get_text(strip=True)
                if text:
                    notifications.append((text, a_tag['href']))
        return notifications
    except Exception as e:
        print("Error fetching data:", e)
        return []

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(telegram_url, json=payload)

if __name__ == "__main__":
    current_list = get_latest_notifications()
    if current_list:
        title, link_sub = current_list[0]
        full_link = link_sub if link_sub.startswith("http") else f"https://www.tnpsc.gov.in/{link_sub}"
        
        message = f"🚨 *TNPSC Latest Check!*\n\n📌 *Title:* {title}\n🔗 *Link:* {full_link}"
        send_telegram_message(message)
        print("Message sent successfully!")
    else:
        print("No notifications found.")
