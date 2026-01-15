# main.py (FULL FIXED)
# ✅ Render-ready
# ✅ FIX Embed syntax
# ✅ Buttons download style (เหมือนเดิม)
# ✅ Split buttons into 2 messages (Discord max 5 buttons per view)
# ✅ Persistent anti-duplicate
# ✅ LINE notify
# ✅ Optional keep_alive

import os
import json
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands

# -------------------------
# Optional keep_alive
# -------------------------
try:
    from web_server import keep_alive
except Exception:
    keep_alive = None


# =========================
# ENV
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
# PERSIST (ANTI DUP)
# =========================
PROCESSED_FILE = "processed_users.json"

def load_processed() -> set[int]:
    try:
        if not os.path.exists(PROCESSED_FILE):
            return set()
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return set(int(x) for x in data)
        if isinstance(data, dict) and "ids" in data and isinstance(data["ids"], list):
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
        print("❌ ไม่พบ LINE_CHANNEL_TOKEN หรือ LINE_USER_ID (ข้าม LINE notify)")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"to": LINE_USER_ID, "messages": [{"type": "text", "text": message}]}

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
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมใช้งานแล้ว!")
    print("🟢 Listening for member role updates...")


def build_welcome_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับเข้าสู่สังกัด ชัชกากาโก",
        description=(
            "ยินดีต้อนรับทุกคนเข้าสู่สังกัด **ชัชกากาโก** 🎊\n"
            "ดาวน์โหลดโปรแกรมและดูคลิปสอนได้จากปุ่มด้านล่างเลยครับ\n"
            "📌 ดูคลิปให้ละเอียด หากติดปัญหาทักผมมาส่วนตัวได้เลยครับ"
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

    return embed


def build_download_view() -> discord.ui.View:
    # ✅ ปุ่มดาวน์โหลด 3 ปุ่ม (ไม่เกิน 5)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="📥 ดาวน์โหลดโปรแกรมรวมเซิฟ",
        url="https://drive.google.com/file/d/17IjFOW0X_ldArpYyLLw75mSNUwyCnwjL/view?usp=sharing",
    ))
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="📥 ดาวน์โหลดโปรแกรมนับวิน",
        url="https://drive.google.com/file/d/1k3KcWUZoxRaGdit7Rf57-1nLe7XRVrcj/view?usp=sharing",
    ))
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="📥 ดาวน์โหลดโปรแกรมของขวัญ",
        url="https://drive.google.com/file/d/1HGh9qTQ1ANwPp9TZE-SDC8Olm7c9dckj/view?usp=sharing",
    ))
    return view


def build_help_view() -> discord.ui.View:
    # ✅ ปุ่มคลิป + กลุ่มไลน์ (4 ปุ่ม)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="📘 คลิปสอน (รวมเซิฟ)",
        url="https://www.youtube.com/watch?v=8EofTTfj1wg",
    ))
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="📘 คลิปสอน (นับวิน)",
        url="https://youtu.be/CVtXY-5Wk4Q",
    ))
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="📘 คลิปสอน (ของขวัญ)",
        url="https://youtu.be/dH4Klh_vODA",
    ))
    view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.link,
        label="📚 เข้ากลุ่ม LINE สังกัด",
        url="https://line.me/ti/g2/C6M5Q-dGYavU6l8zAWQny2zzj4suT0FjdJ6JkA?utm_source=invitation&utm_medium=link_copy&utm_campaign=default",
    ))
    return view


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # roles ไม่เปลี่ยน ข้าม
    if before.roles == after.roles:
        return

    before_roles = {r.id for r in before.roles}
    after_roles = {r.id for r in after.roles}
    new_roles = after_roles - before_roles

    # ตรวจว่าถูกเพิ่ม role ที่เรากำหนด
    if ROLE_ID not in new_roles:
        return

    # กันส่งซ้ำ
    if after.id in already_processed:
        print(f"⚠️ ข้าม {after} เพราะเคยแจ้งแล้ว")
        return

    print(f"🎯 {after} ได้รับ Role ID={ROLE_ID}")

    embed = build_welcome_embed()
    download_view = build_download_view()
    help_view = build_help_view()

    try:
        # ✅ ส่ง 2 ข้อความ เพื่อไม่ชนลิมิตปุ่ม
        await after.send(embed=embed, view=download_view)
        await after.send("📌 ปุ่มคลิปสอน + เข้ากลุ่ม LINE อยู่ด้านล่างครับ", view=help_view)

        print(f"✅ ส่ง DM ให้ {after} สำเร็จ")

        # mark processed เมื่อส่งสำเร็จ
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
        print(f"⛔ ส่ง DM ไม่ได้: {after} (ผู้ใช้อาจปิดรับ DM)")

        granted_time = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%d/%m/%Y %H:%M")
        notify_line(
            "⚠️ DM ส่งไม่สำเร็จ (ผู้ใช้อาจปิดรับ DM)\n\n"
            f"👤 ผู้ใช้: {after.name}\n"
            f"🆔 Discord ID: {after.id}\n"
            f"📌 เวลา: {granted_time}"
        )

    except Exception as e:
        print("⛔ Error on_member_update:", str(e))


# =========================
# KEEP ALIVE (optional)
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
