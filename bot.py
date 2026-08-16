import discord
import os
import requests
from threading import Thread
from flask import Flask

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1525217899973705944
ROLE_ID = 1525217899386507430  # НОВЫЙ ID РОЛИ

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# ===== ВЕБ-СЕРВЕР =====
app = Flask('')

@app.route('/')
def home():
    return "Бот работает"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()
# =======================

def translate_text(text, target_lang='ru'):
    if len(text) > 500:
        text = text[:500] + "..."
    
    try:
        # Google Translate API (бесплатный)
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": target_lang,
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            translated = ""
            for part in data[0]:
                if part[0]:
                    translated += part[0]
            if translated:
                return translated
    except:
        pass
    
    return f"[НЕ УДАЛОСЬ ПЕРЕВЕСТИ] {text}"

@client.event
async def on_ready():
    print(f"Бот {client.user} запущен!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == CHANNEL_ID:
        original_text = message.content

        if not original_text:
            return

        await message.delete()

        translated_text = translate_text(original_text)

        role_mention = f"<@&{ROLE_ID}>"
        await message.channel.send(f"{role_mention}\n📢 **Перевод:**\n{translated_text}")

client.run(TOKEN)
