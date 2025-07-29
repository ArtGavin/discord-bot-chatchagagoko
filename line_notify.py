import os
import requests

# ✅ ส่งข้อความไปยัง LINE Messaging API
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
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message.strip()[:1000]  # ✅ ตัดข้อความไม่ให้เกิน 1000 ตัวอักษร
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ แจ้งเตือน LINE สำเร็จ")
        else:
            print(f"❌ แจ้งเตือน LINE ล้มเหลว ({response.status_code}): {response.text}")
    except Exception as e:
        print("⛔ เกิดข้อผิดพลาดขณะส่ง LINE:", str(e))
