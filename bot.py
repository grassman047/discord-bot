import discord
import os  # Добавляем эту библиотеку для чтения переменных

# Токен теперь берется из переменной окружения, а не пишется здесь
TOKEN = os.getenv('DISCORD_TOKEN')

CHANNEL_ID = 1525217899973705944  # ID канала на твоем сервере
ROLE_ID = 1525217899386507432     # ID твоей роли

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Бот {client.user} запущен!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == CHANNEL_ID and message.flags.crossposted:
        role_mention = f"<@&{ROLE_ID}>"
        await message.channel.send(f"{role_mention}\n{message.content}")

client.run(TOKEN)