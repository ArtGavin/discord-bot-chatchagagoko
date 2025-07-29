import discord
from discord.ext import commands
import os
import requests
from web_server import keep_alive

# ✅ ฟังก์ชันส่งแจ้งเตือนผ่าน LINE Messaging API
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

# ✅ โหลดตัวแปรจาก .env
TOKEN = os.getenv("TOKEN")
ROLE_ID_ENV = os.getenv("ROLE_ID")

if not TOKEN:
    raise ValueError("❌ ไม่พบ TOKEN ใน .env")

if not ROLE_ID_ENV:
    raise ValueError("❌ ไม่พบ ROLE_ID ใน .env")

ROLE_ID = int(ROLE_ID_ENV)

print("🔐 TOKEN Loaded:", TOKEN[:10] + "...")
print("🆔 ROLE_ID Loaded:", ROLE_ID)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมใช้งานแล้ว!")

@bot.event
async def on_member_update(before, after):
    before_roles = set(r.id for r in before.roles)
    after_roles = set(r.id for r in after.roles)

    new_roles = after_roles - before_roles
    if ROLE_ID in new_roles:
        try:
            embed = discord.Embed(
                title="🎉 ยินดีต้อนรับเข้าสู่สังกัด ชัชกากาโก",
                description=(
                    "นี้คือ ไฟล์ โปรแกรม สำหรับ ชาว กากาโก ทุกคน พร้อมคลิปสอน ยินดีต้อนรับทุกคนด้วยครับ ดูคลิปให้ละเอียดนะครับทุกคน ใครไม่ได้ติดตรงไหนทักผมมาส่วนตัวนะครับ:\n\n"
                    "**🧩 โปรแกรมรวมเซิฟ**\n"
                    "📥 **ติดตั้งโปรแกรม:**\n"
                    "👉 [คลิกเพื่อติดตั้ง](https://drive.google.com/file/d/1ci9uRu5TkSpxl8av82TgVSL9R9Xni_VL/view)\n"
                    "📺 **วิธีติดตั้งและใช้งาน:**\n"
                    "🎬 [คลิกเพื่อดูวิดีโอ](https://www.youtube.com/watch?v=8EofTTfj1wg)\n\n"
                    "**⏱️ โปรแกรมนับวิน**\n"
                    "📥 **ติดตั้งโปรแกรม:**\n"
                    "👉 [คลิกเพื่อติดตั้ง](https://www.dropbox.com/scl/fi/xwabt3yle621a8ok82gal/WIN.rar?rlkey=2ijd3wi9en6mt3f1ahd696vji&e=3&st=mzet6r9j&dl=0)\n"
                    "📺 **วิธีติดตั้งและใช้งาน:**\n"
                    "🎬 [คลิกเพื่อดูวิดีโอ](https://youtu.be/pjiswNBf_p8)\n\n"
                    "**🎁 รูปของขวัญ**\n"
                    "🧧 สำหรับผู้ที่ติดตั้งเสร็จแล้ว:\n"
                    "🎁 [รับรูปของขวัญที่นี่](https://drive.google.com/file/d/1lNtyyflKvQ45ik03aeh027SqCVcSKfXX/view)"
                ),
                color=discord.Color.teal()
            )

            embed.set_author(
                name="สังกัดชัชกากาโก",
                icon_url="https://media.discordapp.net/attachments/792173112376426516/1391401833934753802/tiktok-logo-tikok-icon-transparent-tikok-app-logo-free-png.png"
            )

            embed.set_image(
                url="https://media.discordapp.net/attachments/792173112376426516/1399430468650270913/image.png"
            )

            embed.set_footer(
                text="สังกัดชัชกากาโก • 📌หมายเหตุ:หากมีปัญหาในการใช้งาน โปรดติดต่อได้ตลอดเวลา!",
                icon_url="https://media.discordapp.net/attachments/1286230378507669514/1391041551081144423/image-removebg-preview_-_2025-06-14T113430.201.png"
            )

            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="📘 วิธีใช้งานโปรแกรม", url="https://www.youtube.com/watch?v=8EofTTfj1wg"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="📚 ดูข้อมูลเพิ่มเติมในสังกัด", url="https://line.me/ti/g2/C6M5Q-dGYavU6l8zAWQny2zzj4suT0FjdJ6JkA?utm_source=invitation&utm_medium=link_copy&utm_campaign=default"))

            await after.send(embed=embed, view=view)
            print(f"📩 ส่งข้อความ DM ไปยัง {after.name} เรียบร้อย")

            notify_line(f"📩 ส่งข้อความ DM ไปยัง {after.name} เรียบร้อยแล้ว")
        
        except discord.Forbidden:
            print(f"⛔ ไม่สามารถส่ง DM ไปยัง {after.name} ได้ (อาจปิดรับ DM)")

# ✅ ป้องกัน Replit หลับ (หากใช้)
keep_alive()
bot.run(TOKEN)
