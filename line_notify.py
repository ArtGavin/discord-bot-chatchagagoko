import requests
import os

LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")  # ✅ ใช้ชื่อเดียวกับใน Render

def notify_line(message: str):
    token = os.getenv("LINE_CHANNEL_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    if not token or not user_id:
        print("❌ ไม่พบ LINE_CHANNEL_TOKEN หรือ LINE_USER_ID")
        return

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        print(f"✅ แจ้งเตือนไปยัง LINE แล้ว ({res.status_code})")
    except Exception as e:
        print("⛔ แจ้งเตือน LINE ล้มเหลว:", str(e))

