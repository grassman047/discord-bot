import discord
import os
import requests
from threading import Thread
from flask import Flask

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1525217899973705944
ROLE_ID = 1525217899386507432

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

app = Flask('')

@app.route('/')
def home():
    return "Бот работает"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

def translate_text(text, target_lang='ru'):
    print(f"🔍 Пытаюсь перевести: {text[:50]}...")
    
    if len(text) > 500:
        text = text[:500] + "..."
    
    # Google Translate
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": target_lang,
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params, timeout=10)
        print(f"📡 Google ответ: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            translated = ""
            for part in data[0]:
                if part[0]:
                    translated += part[0]
            if translated:
                print(f"✅ Перевод: {translated[:50]}...")
                return translated
    except Exception as e:
        print(f"❌ Google ошибка: {e}")
    
    # LibreTranslate
    try:
        url = "https://translate.argosopentech.com/translate"
        payload = {
            "q": text,
            "source": "en",
            "target": target_lang,
            "format": "text"
        }
        response = requests.post(url, json=payload, timeout=10)
        print(f"📡 Libre ответ: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if "translatedText" in result:
                print(f"✅ Перевод: {result['translatedText'][:50]}...")
                return result["translatedText"]
    except Exception as e:
        print(f"❌ Libre ошибка: {e}")
    
    print("❌ ВСЁ СЛОМАЛОСЬ")
    return f"[НЕ УДАЛОСЬ ПЕРЕВЕСТИ] {text}"

@client.event
async def on_ready():
    print(f"✅ Бот {client.user} запущен!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == CHANNEL_ID:
        print(f"📩 Получено сообщение: {message.content[:50]}...")
        
        original_text = message.content

        if not original_text:
            return

        await message.delete()
        print("🗑️ Сообщение удалено")

        translated_text = translate_text(original_text)

        role_mention = f"<@&{ROLE_ID}>"
        await message.channel.send(f"{role_mention}\n📢 **Перевод:**\n{translated_text}")
        print("✅ Сообщение отправлено с пингом")

client.run(TOKEN)
