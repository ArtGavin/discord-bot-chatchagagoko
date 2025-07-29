import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

# ✅ โหลดตัวแปรจาก .env
TOKEN = os.getenv("TOKEN")
ROLE_ID_ENV = os.getenv("ROLE_ID")

# ✅ ตรวจว่ามีค่าจริงหรือไม่
if not TOKEN:
    raise ValueError("❌ ไม่พบ TOKEN ใน .env")

if not ROLE_ID_ENV:
    raise ValueError("❌ ไม่พบ ROLE_ID ใน .env")

# ✅ แปลงเป็น int
ROLE_ID = int(ROLE_ID_ENV)

# ✅ DEBUG log (สามารถลบได้ภายหลัง)
print("🔐 TOKEN Loaded:", TOKEN[:10] + "...")
print("🆔 ROLE_ID Loaded:", ROLE_ID)

# ✅ ตั้งค่า Bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมใช้งานแล้ว!")

# ... (เหมือนเดิมด้านบน)

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

            # ✅ รูปโปรแกรมหลัก (จะแสดงใต้ Embed)
            embed.set_image(url="https://media.discordapp.net/attachments/123456789012345678/139999999999999999/main-program-preview.png")


            # หัว Embed
            embed.set_author(
                name="สังกัดชัชกากาโก",
                icon_url="https://media.discordapp.net/attachments/792173112376426516/1391401833934753802/tiktok-logo-tikok-icon-transparent-tikok-app-logo-free-png.png"
            )

            # ✅ ภาพหลักด้านล่าง (ขนาดใหญ่)
            embed.set_image(
                url="https://media.discordapp.net/attachments/792173112376426516/1399430468650270913/image.png"
            )

            # ✅ Footer
            embed.set_footer(
                text="สังกัดชัชกากาโก • 📌หมายเหตุ:หากมีปัญหาในการใช้งาน โปรดติดต่อได้ตลอดเวลา!",
                icon_url="https://media.discordapp.net/attachments/1286230378507669514/1391041551081144423/image-removebg-preview_-_2025-06-14T113430.201.png"
            )

            # ✅ ปุ่มสวยงาม
            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="📘 วิธีใช้งานโปรแกรม", url="https://www.youtube.com/watch?v=8EofTTfj1wg"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="📚 ดูข้อมูลเพิ่มเติมในสังกัด", url="https://line.me/ti/g2/C6M5Q-dGYavU6l8zAWQny2zzj4suT0FjdJ6JkA?utm_source=invitation&utm_medium=link_copy&utm_campaign=default"))

            await after.send(embed=embed, view=view)
            print(f"📩 ส่งข้อความ DM ไปยัง {after.name} เรียบร้อย")

        except discord.Forbidden:
            print(f"⛔ ไม่สามารถส่ง DM ไปยัง {after.name} ได้ (อาจปิดรับ DM)")

# ✅ รัน Flask server ป้องกัน Replit หลับ
keep_alive()
bot.run(TOKEN)
