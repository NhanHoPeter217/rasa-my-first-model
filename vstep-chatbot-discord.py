# This example requires the 'message_content' intent.

import discord
import os
from pprint import pprint
import requests

from dotenv import load_dotenv
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

url = 'http://localhost:5005/webhooks/rest/webhook'  # Replace with the actual API endpoint URL

headers = {
  'Content-Type': 'application/json'  # Specify JSON content type
}

def get_response(message, sender='test_user') -> str:
  data = {
    "sender": sender,
    "message": message
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:  # Check for successful request (status code 200)
      data = response.json()
      return data[0]['text']
  else:
      print(f"Discord.py failed, code {response.status_code} || {response.json()}")
      print(response.text)  # Print the error message if available
      return "Error discord.py"


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    res = get_response(message.content, message.author.id)
    await message.channel.send(res)



if (discord_token is None):
    print('DISCORD_TOKEN is not set')
else:
  client.run(discord_token)
