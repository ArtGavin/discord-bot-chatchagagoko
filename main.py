import os
import requests
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from web_server import keep_alive

TZ = ZoneInfo("Asia/Bangkok")

# =========================
# ✅ LINE Messaging API notify
# =========================
def notify_line(message: str):
    token = os.getenv("LINE_CHANNEL_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    if not token or not user_id:
        print("❌ ไม่พบ LINE_CHANNEL_TOKEN หรือ LINE_USER_ID")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}],
    }

    try:
        res = requests.post(url, headers=headers, json=data, timeout=15)
        print(f"✅ แจ้งเตือนไปยัง LINE แล้ว ({res.status_code})")
        if res.status_code >= 400:
            print("⚠️ LINE Response:", res.text[:500])
    except Exception as e:
        print("⛔ แจ้งเตือน LINE ล้มเหลว:", str(e))


# =========================
# ✅ Load env
# =========================
TOKEN = os.getenv("TOKEN")
ROLE_ID_ENV = os.getenv("ROLE_ID")

if not TOKEN:
    raise ValueError("❌ ไม่พบ TOKEN ใน .env (TOKEN)")
if not ROLE_ID_ENV:
    raise ValueError("❌ ไม่พบ ROLE_ID ใน .env (ROLE_ID)")

ROLE_ID = int(ROLE_ID_ENV)

print("🔐 TOKEN Loaded:", TOKEN[:10] + "...")
print("🆔 ROLE_ID Loaded:", ROLE_ID)


# =========================
# ✅ Discord bot setup
# =========================
intents = discord.Intents.default()
intents.members = True  # ต้องเปิดใน Developer Portal ด้วย (Server Members Intent)
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)


# =========================
# ✅ กันส่งซ้ำ (แบบ TTL)
# =========================
# key: user_id, value: datetime_processed
already_processed: dict[int, datetime] = {}
PROCESSED_TTL = timedelta(hours=24)


def cleanup_processed(now: datetime):
    # ลบรายการเก่าออก เพื่อลด memory
    expired = [uid for uid, ts in already_processed.items() if now - ts > PROCESSED_TTL]
    for uid in expired:
        already_processed.pop(uid, None)


# =========================
# ✅ Helpers: Build nice embed
# =========================
def build_welcome_embed(member: discord.Member) -> discord.Embed:
    now = datetime.now(TZ)

    embed = discord.Embed(
        title="🎉 ยินดีต้อนรับเข้าสู่สังกัด ชัชกากาโก",
        description=(
            f"สวัสดีคุณ **{member.display_name}** 👋\n"
            "ยินดีต้อนรับเข้าสู่สังกัด **ชัชกากาโก** 🎊\n\n"
            "ด้านล่างคือไฟล์โปรแกรม + คลิปสอนใช้งานทั้งหมด\n"
            "📌 **แนะนำ:** ดูคลิปก่อนติดตั้งทุกครั้ง เพื่อกันทำผิดขั้นตอน"
        ),
        color=discord.Color.teal(),
        timestamp=now,
    )

    embed.set_author(
        name="สังกัดชัชกากาโก",
        icon_url="https://media.discordapp.net/attachments/792173112376426516/1391401833934753802/tiktok-logo-tikok-icon-transparent-tikok-app-logo-free-png.png",
    )

    # ✅ Fields (ทำให้เหมือนกล่อง/การ์ด)
    embed.add_field(
        name="🧩 โปรแกรมรวมเซิฟ",
        value=(
            "📥 ดาวน์โหลด:\n"
            "https://drive.google.com/file/d/17IjFOW0X_ldArpYyLLw75mSNUwyCnwjL/view?usp=sharing\n\n"
            "🎬 วิธีติดตั้งและใช้งาน:\n"
            "https://www.youtube.com/watch?v=8EofTTfj1wg"
        ),
        inline=False,
    )

    embed.add_field(
        name="⏱️ โปรแกรมนับวิน",
        value=(
            "📥 ดาวน์โหลด:\n"
            "https://drive.google.com/file/d/1k3KcWUZoxRaGdit7Rf57-1nLe7XRVrcj/view?usp=sharing\n\n"
            "🎬 วิธีติดตั้งและใช้งาน:\n"
            "https://youtu.be/CVtXY-5Wk4Q"
        ),
        inline=False,
    )

    embed.add_field(
        name="🎁 โปรแกรมของขวัญ",
        value=(
            "📥 ดาวน์โหลด:\n"
            "https://drive.google.com/file/d/1HGh9qTQ1ANwPp9TZE-SDC8Olm7c9dckj/view?usp=sharing\n\n"
            "🎬 วิธีติดตั้งและใช้งาน:\n"
            "https://youtu.be/dH4Klh_vODA"
        ),
        inline=False,
    )

    embed.set_image(
        url="https://media.discordapp.net/attachments/792173112376426516/1430822820937601065/3c7f3492965159fa.png?format=webp&quality=lossless"
    )

    embed.set_footer(
        text="สังกัดชัชกากาโก • หากมีปัญหาในการใช้งาน ทักได้ตลอดเวลา 💬",
        icon_url="https://media.discordapp.net/attachments/1286230378507669514/1391041551081144423/image-removebg-preview_-_2025-06-14T113430.201.png",
    )

    return embed


def build_welcome_view() -> discord.ui.View:
    view = discord.ui.View()

    view.add_item(
        discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="📘 คลิปวิธีใช้งาน (รวมเซิฟ)",
            url="https://www.youtube.com/watch?v=8EofTTfj1wg",
        )
    )
    view.add_item(
        discord.ui.Button(
            style=discord.ButtonStyle.link,
            label="📚 กลุ่มข้อมูลสังกัด (LINE)",
            url="https://line.me/ti/g2/C6M5Q-dGYavU6l8zAWQny2zzj4suT0FjdJ6JkA?utm_source=invitation&utm_medium=link_copy&utm_campaign=default",
        )
    )

    return view


# =========================
# ✅ Events
# =========================
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมใช้งานแล้ว!")


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # roles ไม่เปลี่ยน = ไม่ต้องทำอะไร
    if before.roles == after.roles:
        return

    now = datetime.now(TZ)
    cleanup_processed(now)

    before_roles = {r.id for r in before.roles}
    after_roles = {r.id for r in after.roles}

    # role ใหม่ที่เพิ่มเข้ามา
    new_roles = after_roles - before_roles

    # เงื่อนไข: ได้ ROLE_ID เพิ่มใหม่จริง
    if ROLE_ID not in new_roles:
        return

    # กันซ้ำ: ถ้าเคยส่งภายใน TTL แล้ว
    if after.id in already_processed:
        print(f"⚠️ ข้าม {after.name} เพราะเคยแจ้งแล้วภายใน {PROCESSED_TTL}")
        return

    already_processed[after.id] = now

    # ✅ สร้าง embed + view
    embed = build_welcome_embed(after)
    view = build_welcome_view()

    try:
        await after.send(embed=embed, view=view)
        print(f"✅ ส่ง DM ต้อนรับให้ {after.name} แล้ว")

        granted_time = now.strftime("%d/%m/%Y %H:%M")
        line_message = (
            "📥 แจ้งเตือนการเข้าร่วมสังกัดใหม่!\n\n"
            f"👤 ผู้ใช้: {after.name}\n"
            f"🆔 Discord ID: {after.id}\n"
            "🏅 ยศที่ได้รับ: สมาชิกกากาโก\n"
            "📦 ส่งข้อความ DM เรียบร้อย ✅\n\n"
            f"📌 เวลาได้รับยศ: {granted_time}"
        )
        notify_line(line_message)

    except discord.Forbidden:
        print(f"⛔ ไม่สามารถส่ง DM ไปยัง {after.name} ได้ (ผู้ใช้อาจปิดรับ DM)")
    except Exception as e:
        print("⛔ Error sending welcome:", str(e))


# =========================
# ✅ keep alive (replit / render)
# =========================
keep_alive()
bot.run(TOKEN)

