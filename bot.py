from dotenv import load_dotenv
load_dotenv()

import discord
import os
import re
from urllib.parse import unquote
from datetime import date, datetime

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ALL_RESULTS_DATES = [
    ("IGCSE (October/November 2025)", "08 January 2026"),
    ("A-Level (January 2026)", "26 February 2026"),
    ("A-Level (May/June 2026)", "13 August 2026"),
    ("IGCSE (May/June 2026)", "20 August 2026"),
    ("IGCSE (October/November 2026)", "15 January 2027"),
    ("A-Level (January 2027)", "11 February 2027"),
]

def get_results_dates():
    today = date.today()
    upcoming = []
    for label, date_str in ALL_RESULTS_DATES:
        target = datetime.strptime(date_str, "%d %B %Y").date()
        if target >= today:
            upcoming.append((label, date_str))
    a = upcoming[0] if len(upcoming) > 0 else (None, None)
    b = upcoming[1] if len(upcoming) > 1 else (None, None)
    return a, b

def days_until(date_str):
    try:
        target = datetime.strptime(date_str, "%d %B %Y").date()
        delta = (target - date.today()).days
        if delta > 0:
            return f"{delta} days away"
        elif delta == 0:
            return "today!"
        else:
            return f"{abs(delta)} days ago"
    except:
        return "?"

def convert_link(raw):
    if "redirect_to=" in raw:
        after = raw.split("redirect_to=", 1)[1]
        decoded = unquote(after)
        return decoded
    return unquote(raw)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(PREFIX):
        return

    content = message.content[len(PREFIX):].strip()
    command = content.split()[0].lower() if content else ""
    args = content[len(command):].strip()

    if command == "convert":
        if not args:
            await message.channel.send("Usage: `!convert <link>`")
            return
        result = convert_link(args)
        await message.channel.send(f"✅ Converted link:\n{result}")

    elif command == "resultsday":
        a, b = get_results_dates()
        lines = ["📅 **Next Oxford AQA Results Days**\n"]
        if a[1]:
            lines.append(f"**{a[0]}:** {a[1]} ({days_until(a[1])})")
        if b[1]:
            lines.append(f"**{b[0]}:** {b[1]} ({days_until(b[1])})")
        if not a[1]:
            lines.append("No upcoming results days found.")
        await message.channel.send("\n".join(lines))

client.run(TOKEN)