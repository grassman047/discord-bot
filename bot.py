import discord
import os
import requests
from threading import Thread
from flask import Flask

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1525217899973705944  # ID канала на твоём сервере
ROLE_ID = 1525217899386507432  # ID твоей роли

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# ===== ВЕБ-СЕРВЕР ДЛЯ RENDER =====
app = Flask('')

@app.route('/')
def home():
    return "Бот работает"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()
# ===================================

def translate_text(text, target_lang='ru'):
    url = "https://libretranslate.com/translate"
    payload = {
        "q": text,
        "source": "en",
        "target": target_lang,
        "format": "text"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["translatedText"]
        else:
            return f"[Ошибка перевода] {text}"
    except Exception:
        return f"[Ошибка соединения] {text}"

@client.event
async def on_ready():
    print(f"Бот {client.user} запущен!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # УБРАЛИ ПРОВЕРКУ НА crossposted
    if message.channel.id == CHANNEL_ID:
        original_text = message.content

        # Пропускаем, если сообщение пустое
        if not original_text:
            return

        await message.delete()

        translated_text = translate_text(original_text)

        role_mention = f"<@&{ROLE_ID}>"
        await message.channel.send(f"{role_mention}\n📢 **Перевод:**\n{translated_text}")

client.run(TOKEN)
