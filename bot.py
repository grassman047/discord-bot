import discord
import os
from threading import Thread
from flask import Flask

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1525217899973705944
ROLE_ID = 1525217899386507432
YOUR_ID = 1003280976811655178  # ЗАМЕНИ НА СВОЙ ID

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

@client.event
async def on_ready():
    print(f"✅ Бот {client.user} готов!")

@client.event
async def on_message(message):
    # 1. Игнорируем сообщения САМОГО БОТА (это главное!)
    if message.author == client.user:
        return

    # 2. Только в нужном канале
    if message.channel.id != CHANNEL_ID:
        return

    # 3. Только от тебя
    if message.author.id != YOUR_ID:
        return

    # 4. Удаляем твоё сообщение
    await message.delete()

    # 5. Отправляем с пингом
    role_mention = f"<@&{ROLE_ID}>"
    await message.channel.send(f"{role_mention}\n{message.content}")
