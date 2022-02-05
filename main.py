import os
import discord
import random
import requests
from trivia_utils import trivia_options, category_options, category_map, difficulty_options_str, difficulty_map, difficulty_options, category_readable
import base64

"""
Google Meets Link
https://meet.google.com/ire-bksc-qgz
"""

"""
Useful links

https://discord.gg/AQZzSg32

CodeCamp Video
https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

Discord Library Docs
https://discordpy.readthedocs.io/en/stable/
"""
"""
Requirements
------------------
1. Called by "~trivia" 

2. Parse difficulty response from messages

3. Only responds to the person who called it initially (need to keep track of the user currently playing)

4. For now, only one trivia game at a time (if a second user invokes the bot with !trivia, the trivia bot will say that its busy right now)


Bells and Whistles (Future Enhancements)
-----------------------------------------
1. later, add support for multiple parallel games 
    - bot will need to mention you in the trivia questions so you know which questions are for you
    - python code will need to keep track of all of the different games going on at once

2. high score list 
  - you can ask the bot for the high score list and it will give it to you

3. Uptime Bot
  - https://uptimerobot.com/

4. Use Repl secrets management for the app token

"""

client = discord.Client()

client.waiting_for_category = False
client.waiting_for_difficulty = False
client.question_number = -1
client.numcorrect = 0


client.category_readable = category_readable
client.category_map = category_map
client.category_map["G"] = random.randint(9, 32)
client.difficulty_map = difficulty_map
client.difficulty_map["D"] = random.choice(["easy", "medium", "hard"])



async def print_question(message):
  ### printing question

  msg = ""

  
  msg += f"{client.question_number+1}. {base64.b64decode(client.questions[client.question_number]['question']).decode('utf-8')}\n"

  possible_answers=client.questions[client.question_number]["incorrect_answers"]
  possible_answers.append(client.questions[client.question_number]["correct_answer"])
  random.shuffle(possible_answers)
  
  client.answer_dict = {}
  letters = ["D","C","B","A"]
  for answer in possible_answers:
    letter = letters.pop()
    client.answer_dict[letter] = answer
    msg+=(f"{letter}. {base64.b64decode(answer).decode('utf-8')}\n")
    
  msg+=(f"  Select your answer:  ")
  await message.channel.send(msg)


@client.event
async def on_ready():
  print(f"Logged on as {client.user}!")

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith("~Trivia") or message.content.startswith("~trivia"):
    client.question_number =-1
    client.numcorrect = 0
    client.waiting_for_category = True
    client.initial_user = message.author
    await message.channel.send(trivia_options)
  
  elif message.content.startswith("~") and message.author == client.initial_user:
    if client.waiting_for_category:
      msg = message.content[1:]
      if msg.upper() in category_options:
        if msg.upper() in client.category_map.keys():
          client.category_str = str(client.category_map[msg.upper()])
        elif msg.upper() == "H":
          client.category_str = ""
        client.waiting_for_category = False
        client.waiting_for_difficulty = True
        await message.channel.send(f"That was a valid choice: you chose category {client.category_readable[msg.upper()]}")
        await message.channel.send(difficulty_options_str)
      else:
        await message.channel.send(" Perhaps put in a valid answer. ")
        await message.channel.send(trivia_options)
        
    elif client.waiting_for_difficulty:
      msg = message.content[1:]
      if msg.upper() in difficulty_options:
        if msg.upper() in client.difficulty_map.keys():
          client.difficulty_str = str(client.difficulty_map[msg.upper()])
        elif msg.upper() == "E":
          client.difficulty_str = ""
        client.waiting_for_difficulty = False
        await message.channel.send(f"That was a valid choice: you chose difficulty  {client.difficulty_str}")
        
        url = f"https://opentdb.com/api.php?amount=10&category={client.category_str}&difficulty={client.difficulty_str}&type=multiple&encode=base64"
        
        client.questions = requests.get(url).json()["results"]
        client.question_number += 1
        
        await print_question(message)
        
    elif client.question_number >= 0:
      msg = message.content[1:]
      if msg.upper() in client.answer_dict.keys():
        user_answer = client.answer_dict[msg.upper()]
        if user_answer==client.questions[client.question_number]["correct_answer"]:
          client.numcorrect+=1
          await message.channel.send(f" Correct! {client.numcorrect}/{client.question_number+1}")
        else:
          await message.channel.send(f" Incorrect. {client.numcorrect}/{client.question_number+1}")
        client.question_number += 1
        if client.question_number >= 10:
          await message.channel.send( "Game Over! ")
        else:
          await print_question(message)
      else:
        await message.channel.send(" Perhaps put in a valid answer. ")
        await print_question(message)
      
  print(f"Message from {message.author}: {message.content}")

my_secret = os.environ['DISCORD_TOKEN']
client.run(my_secret)






