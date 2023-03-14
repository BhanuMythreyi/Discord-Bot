import discord
import os
import requests
import json
import random
import wikipedia
import datetime
import smtplib # simple mail transfer protocol


server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

gratitude_words = ["thank","awesome","cool","impressive","nice","happy","good","tq","Bye"]

response_words = ["My pleasure :)","Most Welcome :)","I am here for you :)","Anytime :)"]

negative_words = ["bad","irritating","hate","not good","worst"]

neg_response_words = ["I am sorry for that","I always want to help you","I should have not made that impression"]

client = discord.Client(intents=discord.Intents.all())

# start bot on ready
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - "+json_data[0]['a']
  return(quote)

@client.event
async def on_message(message):
  flag = 0
  if message.author == client.user:
    flag = 1
    return

  if message.content.lower().startswith('hi'):
    await message.channel.send('Hello, How can I help you!!')
    flag = 1

  if message.content.lower().startswith('how are you'):
    await message.channel.send('I am cool!!, Thanks for that')
    flag = 1

  if message.content.startswith('inspire'):
    quote = get_quote()
    await message.channel.send(quote)
    flag = 1

  if any(word in message.content for word in negative_words) and "you" in message.content.lower():
    await message.channel.send(random.choice(neg_response_words))
    flag = 1

  if any(word in message.content for word in gratitude_words) and "you" in message.content.lower():
    await message.channel.send(random.choice(response_words))
    flag = 1


  if 'what' and 'is' and 'time' in message.content:
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    await message.channel.send(f'The time is {strTime}')
    flag = 1
    
  if "?" in message.content or "meaning" in message.content.lower():
    query = message.content.replace("wikipedia","")
    results = wikipedia.summary(query,sentences=2)
    await message.channel.send("According to wikipedia")
    await message.channel.send(results)
    flag = 1

  if "*ADMIN-RESPONSE-REQUIRED" in message.content:

    # Some important details that admin has to address then bot has to send an email to admin -- key (ADMIN RESPONSE REQUIRED) --> ask user to end text with *ADMIN-RESPONSE-REQUIRED, the the content will be stripped and a mail will be sent to the pre defined email id
    
    sender_mail = "discorddemo@gmail.com"
    sender_password = "passworddemo"
    receiver_mail = "project@gmail.com"
    server.login(sender_mail,sender_password)
    
    mail_content = ""
    cont = message.content.split(" ")
    for i in cont:
      if i != "*ADMIN-RESPONSE-REQUIRED":
        mail_content += i+" "
    server.sendmail(sender_mail,receiver_mail,mail_content)
    await message.channel.send("Your query has been sent to the admin. Please hold on for their response")
    flag = 1

  
  if flag==0:
    channel = client.get_channel(1078964071317118976)
    await channel.send(message.content)

  

client.run(os.getenv('TOKEN'))
