# main.py (FULL FIXED for Render)
# - Fix Embed syntax (missing commas)
# - Persistent "already_processed" (survives restarts)
# - Clear logs
# - Safe LINE notify
# - keep_alive support

import os
import json
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands

# ถ้ามีไฟล์ web_server.py (Flask keep alive) ให้ใช้งานได้
# ถ้าไม่มี จะข้ามแบบไม่พัง
try:
    from web_server import keep_alive
except Exception:
    keep_alive = None


# =========================
# CONFIG / ENV
# =========================
TOKEN = os.getenv("TOKEN")
ROLE_ID_ENV = os.getenv("ROLE_ID")

LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

if not TOKEN:
    raise ValueError("❌ ไม่พบ TOKEN ใน Environment (Render -> Environment)")
if not ROLE_ID_ENV:
    raise ValueError("❌ ไม่พบ ROLE_ID ใน Environment (Render -> Environment)")

ROLE_ID = int(ROLE_ID_ENV)

print("🔐 TOKEN Loaded:", TOKEN[:10] + "...")
print("🆔 ROLE_ID Loaded:", ROLE_ID)


# =========================
# PERSIST STORE (ANTI DUP)
# =========================
PROCESSED_FILE = "processed_users.json"

def load_processed() -> set[int]:
    try:
        if not os.path.exists(PROCESSED_FILE):
            return set()
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # รองรับทั้ง list / dict เผื่อเคยเปลี่ยน format
        if isinstance(data, list):
            return set(int(x) for x in data)
        if isinstance(data, dict) and "ids" in data:
            return set(int(x) for x in data["ids"])
        return set()
    except Exception as e:
        print("⚠️ โหลด processed_users.json ไม่ได้:", str(e))
        return set()

def save_processed(ids: set[int]) -> None:
    try:
        with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(list(ids)), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("⚠️ เซฟ processed_users.json ไม่ได้:", str(e))


already_processed: set[int] = load_processed()
print(f"🧠 loaded already_processed: {len(already_processed)} users")


# =========================
# LINE NOTIFY
# =========================
def notify_line(message: str) -> None:
    if not LINE_CHANNEL_TOKEN or not LINE_USER_ID:
        print("❌ ไม่พบ LINE_CHANNEL_TOKEN หรือ LINE_USER_ID (ข้ามการแจ้งเตือน LINE)")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}],
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"✅ แจ้งเตือนไปยัง LINE แล้ว ({res.status_code})")
        if res.status_code >= 400:
            print("⚠️ LINE response:", res.text[:500])
    except Exception as e:
        print("⛔ แจ้งเตือน LINE ล้มเหลว:", str(e))


# =========================
# DISCORD BOT
# =========================
intents = discord.Intents.default()
intents.members = True
intents.guilds = True  # กันบางเคส event ไม่ยิง

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมใช้งานแล้ว!")
    print("🟢 Listening for role updates...")


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # กัน event ยิงแต่ roles เหมือนเดิม
    if before.roles == after.roles:
        return

    before_roles = {r.id for r in before.roles}
    after_roles = {r.id for r in after.roles}

    new_roles = after_roles - before_roles

    # โดนเพิ่ม ROLE_ID เข้ามา
    if ROLE_ID not in new_roles:
        return

    # กันส่งซ้ำ (persist)
    if after.id in already_processed:
        print(f"⚠️ ข้าม {after} เพราะเคยแจ้งแล้ว")
        return

    print(f"🎯 ตรวจพบ {after} ได้รับ Role ID={ROLE_ID}")

    # --- สร้าง Embed ---
    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับเข้าสู่สังกัด ชัชกากาโก",
        description=(
            "ยินดีต้อนรับทุกคนเข้าสู่สังกัด **ชัชกากาโก** 🎊\n"
            "ไฟล์โปรแกรมและคลิปสอนใช้งานทั้งหมดอยู่ด้านล่างนี้\n"
            "📌 กรุณาดูคลิปให้ละเอียด หากติดปัญหาจุดไหนสามารถทักผมมาส่วนตัวได้เลยครับ\n\n"

            "🧩 **โปรแกรมรวมเซิฟ**\n\n"
            "📥 **ดาวน์โหลดโปรแกรม**\n"
            "👉 https://drive.google.com/file/d/17IjFOW0X_ldArpYyLLw75mSNUwyCnwjL/view?usp=sharing\n\n"
            "📺 **วิธีติดตั้งและใช้งาน**\n"
            "🎬 https://www.youtube.com/watch?v=8EofTTfj1wg\n\n"

            "⏱️ **โปรแกรมนับวิน**\n\n"
            "📥 **ดาวน์โหลดโปรแกรม**\n"
            "👉 https://drive.google.com/file/d/1k3KcWUZoxRaGdit7Rf57-1nLe7XRVrcj/view?usp=sharing\n\n"
            "📺 **วิธีติดตั้งและใช้งาน**\n"
            "🎬 https://youtu.be/CVtXY-5Wk4Q\n\n"

            "🎁 **โปรแกรมของขวัญ**\n\n"
            "📥 **ดาวน์โหลดโปรแกรม**\n"
            "👉 https://drive.google.com/file/d/1HGh9qTQ1ANwPp9TZE-SDC8Olm7c9dckj/view?usp=sharing\n\n"
            "📺 **วิธีติดตั้งและใช้งาน**\n"
            "🎬 https://youtu.be/dH4Klh_vODA"
        ),
        color=discord.Color.teal(),
    )

    embed.set_author(
        name="สังกัดชัชกากาโก",
        icon_url="https://media.discordapp.net/attachments/792173112376426516/1391401833934753802/tiktok-logo-tikok-icon-transparent-tikok-app-logo-free-png.png",
    )

    embed.set_image(
        url="https://media.discordapp.net/attachments/792173112376426516/1430822820937601065/3c7f3492965159fa.png?format=webp&quality=lossless"
    )

    embed.set_footer(
        text="สังกัดชัชกากาโก • 📌หมายเหตุ:หากมีปัญหาในการใช้งาน โปรดติดต่อได้ตลอดเวลา!",
        icon_url="https://media.discordapp.net/attachments/1286230378507669514/1391041551081144423/image-removebg-preview_-_2025-06-14T113430.201.png",
    )

    # ปุ่มลิงก์
    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="📘 วิธีใช้งานโปรแกรม",
            url="https://www.youtube.com/watch?v=8EofTTfj1wg",
        )
    )
    view.add_item(
        discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="📚 ดูข้อมูลเพิ่มเติมในสังกัด",
            url="https://line.me/ti/g2/C6M5Q-dGYavU6l8zAWQny2zzj4suT0FjdJ6JkA?utm_source=invitation&utm_medium=link_copy&utm_campaign=default",
        )
    )

    # --- ส่ง DM + LINE ---
    try:
        await after.send(embed=embed, view=view)
        print(f"✅ ส่ง DM ให้ {after} สำเร็จ")

        # mark processed เมื่อ DM ส่งสำเร็จ (หรือจะ mark ก่อนก็ได้)
        already_processed.add(after.id)
        save_processed(already_processed)

        granted_time = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d/%m/%Y %H:%M")
        line_message = (
            "📥 แจ้งเตือนการเข้าร่วมสังกัดใหม่!\n\n"
            f"👤 ผู้ใช้: {after.name}\n"
            f"🆔 Discord ID: {after.id}\n"
            f"🏅 ยศที่ได้รับ: สมาชิกกากาโก\n"
            f"📦 ส่งข้อความ DM เรียบร้อย ✅\n\n"
            f"📌 เวลาได้รับยศ: {granted_time}"
        )
        notify_line(line_message)

    except discord.Forbidden:
        # ถ้าส่ง DM ไม่ได้ จะยังไม่ mark processed เพื่อให้ลองใหม่ภายหลัง (คุณเลือกได้)
        print(f"⛔ ไม่สามารถส่ง DM ไปยัง {after} ได้ (อาจปิดรับ DM)")
        granted_time = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d/%m/%Y %H:%M")
        notify_line(
            "⚠️ DM ส่งไม่สำเร็จ (ผู้ใช้อาจปิดรับ DM)\n\n"
            f"👤 ผู้ใช้: {after.name}\n"
            f"🆔 Discord ID: {after.id}\n"
            f"📌 เวลา: {granted_time}"
        )

    except Exception as e:
        print("⛔ เกิดข้อผิดพลาดใน on_member_update:", str(e))


# =========================
# KEEP ALIVE (Render)
# =========================
if keep_alive:
    try:
        keep_alive()
        print("🌐 keep_alive started")
    except Exception as e:
        print("⚠️ keep_alive start failed:", str(e))
else:
    print("ℹ️ ไม่พบ web_server.keep_alive (ข้าม)")

bot.run(TOKEN)
