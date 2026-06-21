"""
MineRise Discord Welcome Bot
=============================
Sends an instant welcome message to channel 1432803959256645645
when a new member joins the server.

Requirements: pip install discord.py
Run:          python discord_welcome_bot.py
"""

import os
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ─── LOAD .ENV ───────────────────────────────────────────────────────────────
load_dotenv()

# ─── CONFIGURATION ───────────────────────────────────────────────────────────
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
WELCOME_CHANNEL_ID = 1432803959256645645    # Target channel ID

# ─── HUNGARIAN HELPERS ────────────────────────────────────────────────────────

HONAPOK = {
    1: "január", 2: "február", 3: "március", 4: "április",
    5: "május", 6: "június", 7: "július", 8: "augusztus",
    9: "szeptember", 10: "október", 11: "november", 12: "december",
}


def _hungarian_relative_datetime(dt: datetime, now: datetime) -> str:
    """Return a Hungarian-formatted string like:
       '2026. június 22. • ma 14:30-kor'
       '2026. június 21. • tegnap 9:15-kor'
       '2026. június 20. • 18:45-kor'
    """
    date_str = f"{dt.year}. {HONAPOK[dt.month]} {dt.day}."
    time_str = f"{dt.hour}:{dt.minute:02d}-kor"

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    join_start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    day_diff = (today_start - join_start).days

    if day_diff == 0:
        relative = "ma"
    elif day_diff == 1:
        relative = "tegnap"
    elif day_diff == 2:
        relative = "tegnapelőtt"
    else:
        relative = None  # just use the date, no relative word

    if relative:
        return f"{date_str} • {relative} {time_str}"
    return f"{date_str} • {time_str}"


# ─── BOT SETUP ────────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.members = True  # Required to receive on_member_join events
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Called once the bot has logged in successfully."""
    print(f"✅ Bot bejelentkezve: {bot.user} (ID: {bot.user.id})")
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        print(f"⚠️  Nem található a csatorna: {WELCOME_CHANNEL_ID}")
    else:
        print(f"✅ Üdvözlő csatorna megtalálva: #{channel.name}")
    print("🚀 Bot készen áll, várakozás új tagokra...")


@bot.event
async def on_member_join(member: discord.Member):
    """Called every time a new member joins the guild."""
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        print(f"⚠️  Csatorna nem található ({WELCOME_CHANNEL_ID}), üzenet nem küldhető.")
        return

    # Member count (includes the new member)
    guild = member.guild
    member_count = guild.member_count

    # Hungarian-formatted timestamp of when they joined
    now = datetime.now(member.joined_at.tzinfo) if member.joined_at.tzinfo else datetime.now()
    timestamp_str = _hungarian_relative_datetime(member.joined_at, now)

    # Build the welcome message
    welcome_message = (
        f"⚔️ Új harcos érkezett a MineRise-ra!\n"
        f"Üdv a szerveren, {member.mention}, te vagy a {member_count}. tagunk!\n"
        f"Szerverrel kapcsolatos információk:\n\n"
        f"🔋 Csatlakozás: play.balkercraft.eu\n"
        f"🌐 Discord: dsc.gg/MineRise\n"
        f"🛒 Webshop: minerise.szerver.shop\n\n"
        f"Örülünk, hogy itt vagy. Nézz körül, érezd jól magad a MineRise közösségben.\n"
        f"Felhasználó ID: {member.id} - {timestamp_str}"
    )

    try:
        await channel.send(welcome_message)
        print(f"📩 Üdvözlő üzenet elküldve: {member.name} ({member.id})")
    except discord.Forbidden:
        print(f"❌ Nincs engedély üzenetküldésre a csatornában: {WELCOME_CHANNEL_ID}")
    except Exception as e:
        print(f"❌ Hiba az üzenet küldésekor: {e}")


# ─── RUN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("⚠️  DISCORD_BOT_TOKEN nincs beállítva a .env fájlban!")
    else:
        bot.run(BOT_TOKEN)
