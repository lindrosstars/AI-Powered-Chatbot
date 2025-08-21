import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import traceback

# --- Configuration ---
# Your dedicated channel's ID
TARGET_CHANNEL_ID =

# The URL of your n8n webhook
N8N_WEBHOOK_URL = ''

# Define the bot's intents and command prefix
intents = discord.Intents.default()
intents.message_content = True # Required to read message content
intents.messages = True
intents.guilds = True

# Create a bot instance with a command prefix (though we'll handle prefixes in on_message)
bot = commands.Bot(command_prefix='!', intents=intents)

# The 'on_ready' event is called when the bot has connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Target Channel ID: {TARGET_CHANNEL_ID}')

# The 'on_message' event is called whenever a message is sent in any channel the bot can see
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself to prevent infinite loops
    if message.author == bot.user:
        return

    # Check if the message is in the target channel
    if message.channel.id == TARGET_CHANNEL_ID:
        # Check if the message starts with one of our defined commands
        # We're checking the raw message content here
        if message.content.startswith('!gemini') or \
           message.content.startswith('!mistral') or \
           message.content.startswith('!groq'):

            full_command_message = message.content # Get the entire message including the command
            print(f"Detected command from {message.author}: {full_command_message}")

            try:
                payload = {
                    # Send the entire message content to n8n
                    # n8n's Switch node will then determine the command
                    "message_content": full_command_message,
                    "channel_id": message.channel.id,
                    "author_id": message.author.id,
                    "message_id": message.id
                }

                # Send a POST request to the n8n webhook
                requests.post(N8N_WEBHOOK_URL, json=payload)
                print(f"Forwarded payload to n8n: {payload}")

            except Exception as e:
                await message.channel.send(f"An error occurred while forwarding your request: {e}")
                print(f"Error forwarding message: {e}")
                traceback.print_exc()
        # If it's not one of our commands, let the bot's command handler process it
        else:
            await bot.process_commands(message) # This allows other @bot.command() decorators to work if you add them later

# in a try-except block to catch any startup or low-level exceptions.
try:

    load_dotenv() # Make sure your .env file is in the same directory as bot.py
    token = os.getenv('DISCORD_TOKEN')

    if token is None:
        raise ValueError("DISCORD_TOKEN environment variable not set. Please create a .env file or set the variable.")

    bot.run(token)
except ValueError as ve:
    print(f"Configuration Error: {ve}")
except Exception as e:
    print("An unhandled exception occurred during bot startup.")
    traceback.print_exc()