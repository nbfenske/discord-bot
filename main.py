import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

stink_words = ["stink", "stinky", "smelly", "smells", "smell", "stench", "odor"]

stinky_responses = [
  "tbh dominic smells so bad omfg :rofl:",
  "fenske literally smells so good the definition of stink is not fenske if u look it up",
  "omg peee-yew!!! :nauseated_face: dom smells SOOOOOO bad!"
]

starter_sass = [
  "u stink kek",
  "ur nan"
]

def get_gif():
  params = dict(key=os.getenv('GIFAPI'), tag='party')
  response = requests.get("http://api.giphy.com/v1/gifs/random", params=params)
  json_data = json.loads(response.text)
  return(json_data['data']['url'])

def update_sass(user_sass):
  if "sass" in db.keys():
    sass = db["sass"]
    sass.append(user_sass)
    db["sass"] = sass
  else:
    db["sass"] = [user_sass]

def delete_sass(index):
  sass = db["sass"]
  if len(sass) > index:
    del sass[index]
    db["sass"] = sass

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  msg = message.content

  if message.author == client.user:
    return


  if any(word in msg for word in stink_words) or msg.startswith('!stink'):
    if message.author == "DoM#9534":
      await message.channel.send("shut up dom")
    else:
      await message.channel.send(random.choice(stinky_responses))

  if msg.startswith('!fensketime'):
    gif_url = get_gif()
    await message.channel.send(gif_url)

  options = starter_sass
  if "sass" in db.keys():
    options = options + db["sass"]

  if msg.startswith('!sassme'):
    await message.channel.send(random.choice(options))

  if msg.startswith('!showsass'):
    if "sass" in db.keys():
      for (i, item) in enumerate(db["sass"], start=0):
        await message.channel.send(f"{i}: {item}")
    else:
      await message.channel.send("No sass to display. Add some with '!addsass'")

  if msg.startswith('!addsass'):
    new_sass = msg.split("!addsass ",1)[1]
    update_sass(new_sass)
    await message.channel.send("Sass added.")

  if msg.startswith("!rmsass"):
    if "sass" in db.keys():
      sass_index = int(msg.split("!rmsass ", 1)[1])
      delete_sass(sass_index)
      await message.channel.send("Sass removed.")
    else:
      await message.channel.send("No sass to remove. Add some with '!addsass'")

  if msg.startswith("!help"):
    await message.channel.send("!sassme - get some sass")
    await message.channel.send("!addsass <message> - upload some sass")
    await message.channel.send("!showsass - shows the current sass list")
    await message.channel.send("!rmsass <index> - remove sass using the list index from !showsass")
    await message.channel.send("!fensketime - you already know bb")
  
keep_alive()
client.run(os.getenv('TOKEN'))