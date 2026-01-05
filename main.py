import discord
from discord.ext import commands
import os
import requests
from datetime import datetime  # ✅ เพิ่มเพื่อใช้ datetime.now()
from web_server import keep_alive
from zoneinfo import ZoneInfo

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

# ✅ ป้องกันการส่งซ้ำ
already_processed = set()

@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมใช้งานแล้ว!")

@bot.event
async def on_member_update(before, after):
    if before.roles == after.roles:
        return

    before_roles = set(r.id for r in before.roles)
    after_roles = set(r.id for r in after.roles)

    new_roles = after_roles - before_roles
    if ROLE_ID in new_roles and ROLE_ID not in before_roles:

        if after.id in already_processed:
            print(f"⚠️ ข้าม {after.name} เพราะเคยแจ้งแล้ว")
            return

        already_processed.add(after.id)

        try:
            embed = discord.Embed(
                title = "🎉 ยินดีต้อนรับเข้าสู่สังกัด ชัชกากาโก"
                description = (
                    "ยินดีต้อนรับทุกคนเข้าสู่สังกัด **ชัชกากาโก** 🎊\n"
                    "ไฟล์โปรแกรมและคลิปสอนใช้งานทั้งหมดอยู่ด้านล่างนี้\n"
                    "📌 กรุณาดูคลิปให้ละเอียด หากติดปัญหาจุดไหนสามารถทักผมมาส่วนตัวได้เลยครับ\n\n"
                
                    "━━━━━━━━━━━━━━━━━━━\n"
                    "🧩 **โปรแกรมรวมเซิฟ**\n\n"
                    "📥 **ดาวน์โหลดโปรแกรม**\n"
                    "👉 https://drive.google.com/file/d/17IjFOW0X_ldArpYyLLw75mSNUwyCnwjL/view?usp=sharing\n\n"
                    "📺 **วิธีติดตั้งและใช้งาน**\n"
                    "🎬 https://www.youtube.com/watch?v=8EofTTfj1wg\n\n"
                
                    "━━━━━━━━━━━━━━━━━━━\n"
                    "⏱️ **โปรแกรมนับวิน**\n\n"
                    "📥 **ดาวน์โหลดโปรแกรม**\n"
                    "👉 https://drive.google.com/file/d/1k3KcWUZoxRaGdit7Rf57-1nLe7XRVrcj/view?usp=sharing\n\n"
                    "📺 **วิธีติดตั้งและใช้งาน**\n"
                    "🎬 https://youtu.be/CVtXY-5Wk4Q\n\n"
                
                    "━━━━━━━━━━━━━━━━━━━\n"
                    "🎁 **โปรแกรมของขวัญ**\n\n"
                    "📥 **ดาวน์โหลดโปรแกรม**\n"
                    "👉 https://drive.google.com/file/d/1FbjtsWD_FiSnrrfkbPU1wHZHfiiXkFkr/view?usp=sharing\n\n"
                    "📺 **วิธีติดตั้งและใช้งาน**\n"
                    "🎬 https://youtu.be/dH4Klh_vODA\n"
                )
                color=discord.Color.teal()
            )

            embed.set_author(
                name="สังกัดชัชกากาโก",
                icon_url="https://media.discordapp.net/attachments/792173112376426516/1391401833934753802/tiktok-logo-tikok-icon-transparent-tikok-app-logo-free-png.png"
            )

            embed.set_image(
                url="https://media.discordapp.net/attachments/792173112376426516/1430822820937601065/3c7f3492965159fa.png?ex=68fb2d17&is=68f9db97&hm=60fd12906bd06316fdbdbafc6187165cb820f9f7d630b9f1043d56be31ed9f6d&=&format=webp&quality=lossless"
            )

            embed.set_footer(
                text="สังกัดชัชกากาโก • 📌หมายเหตุ:หากมีปัญหาในการใช้งาน โปรดติดต่อได้ตลอดเวลา!",
                icon_url="https://media.discordapp.net/attachments/1286230378507669514/1391041551081144423/image-removebg-preview_-_2025-06-14T113430.201.png"
            )

            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="📘 วิธีใช้งานโปรแกรม", url="https://www.youtube.com/watch?v=8EofTTfj1wg"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="📚 ดูข้อมูลเพิ่มเติมในสังกัด", url="https://line.me/ti/g2/C6M5Q-dGYavU6l8zAWQny2zzj4suT0FjdJ6JkA?utm_source=invitation&utm_medium=link_copy&utm_campaign=default"))

            await after.send(embed=embed, view=view)

            granted_time = datetime.now(ZoneInfo("Asia/Bangkok")).strftime('%d/%m/%Y %H:%M')
            line_message = (
                "📥 *แจ้งเตือนการเข้าร่วมสังกัดใหม่!*\n\n"
                
                f"👤 ผู้ใช้: {after.name}\n"
                f"🆔 Discord ID: {after.id}\n"
                
                f"🏅 ยศที่ได้รับ: สมาชิกกากาโก\n"
                f"📦 ส่งข้อความ DM เรียบร้อย ✅\n\n"
                
                f"📌 เวลาได้รับยศ: {granted_time}"
            )
            notify_line(line_message)

        except discord.Forbidden:
            print(f"⛔ ไม่สามารถส่ง DM ไปยัง {after.name} ได้ (อาจปิดรับ DM)")

# ✅ ป้องกัน Replit หรือ Render หลับ
keep_alive()
bot.run(TOKEN)





























