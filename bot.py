import discord
import os
from threading import Thread
from flask import Flask

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1525217899973705944  # КАНАЛ #апдейты-jjs
ROLE_ID = 1525217899386507432  # РОЛЬ

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
    if message.author == client.user:
        return

    # ТОЛЬКО В ЭТОМ КАНАЛЕ
    if message.channel.id != CHANNEL_ID:
        return

    # ТОЛЬКО ТЫ (замени на свой ID)
    if message.author.id != 1003280976811655178:  # ЗАМЕНИ НА СВОЙ ID
        return

    # Удаляем твоё сообщение
    await message.delete()

    # Отправляем с пингом роли
    role_mention = f"<@&{ROLE_ID}>"
    await message.channel.send(f"{role_mention}\n{message.content}")

client.run(TOKEN)
