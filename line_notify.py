import requests
import os

LINE_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")  # ✅ ใช้ชื่อเดียวกับใน Render

def notify_line(user_id, message: str):
    if not LINE_ACCESS_TOKEN:
        print("❌ ไม่พบ LINE_CHANNEL_TOKEN ใน environment variables")
        return

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}',
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
        print("❌ แจ้งเตือนไม่สำเร็จ:", str(e))
