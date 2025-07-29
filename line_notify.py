import requests
import os

LINE_ACCESS_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

def notify_line(message: str):
    if not LINE_ACCESS_TOKEN:
        print("❌ ไม่พบ LINE_NOTIFY_TOKEN ใน environment variables")
        return

    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'message': message}
    try:
        res = requests.post(url, headers=headers, data=data)
        print(f"✅ แจ้งเตือน LINE แล้ว ({res.status_code})")
    except Exception as e:
        print("❌ แจ้งเตือนไม่สำเร็จ:", str(e))
