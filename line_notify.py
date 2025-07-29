import requests
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ โหลดค่าจาก .env

LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")

def notify_line(user_id, message: str):
    if not LINE_ACCESS_TOKEN:
        print("❌ ไม่พบ LINE_CHANNEL_TOKEN")
        return

    print("📨 กำลังส่ง LINE...")
    print("➡ user_id:", user_id)
    print("➡ message:", message)

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        print(f"✅ แจ้งเตือน LINE แล้ว: {res.status_code} {res.text}")
    except Exception as e:
        print("❌ แจ้งเตือนไม่สำเร็จ:", str(e))
