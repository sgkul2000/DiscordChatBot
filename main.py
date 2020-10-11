from os import environ
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import Bot
import random
from commands.main import *
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import html

	
TOKEN = environ['DISCORD']

client = discord.Client()

chatbot = ChatBot('Roden')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")


@client.event
async def on_ready():
	print(f'{client.user} has connected')
	await client.change_presence(activity=discord.Streaming(name="your mom!", game="Strawberry flavour🍓", url="https://www.twitch.tv/shroud", twitch_name="cruelKarni"), status=discord.Status.idle)


@client.event
async def on_member_join(member):
    response = "Welcome <@"+str(member.id)+">, "+getInsult()
    for channel in member.guild.channels:
        if channel.name == 'general':
            await channel.send(response)


@client.event
@commands.cooldown(1, 30, commands.BucketType.user)
async def on_message(message):
	if message.author == client.user:
		return
	msg = message.content.strip()
	tts = False if ' ' in msg and "notts" in msg.split(" ") else True
	if msg.startswith('!'):
		response = getCommandResponse(msg, message, client)
		await message.delete()
		if(type(response) == discord.Embed):
			newmessage = await message.channel.send(embed=response)
			await newmessage.delete(delay=20)
		elif type(response)==list:
			await message.channel.send(response[0], tts=tts)
			await message.channel.send(response[1], tts=tts)
		else:
			await message.channel.send(html.unescape(response), tts=tts)
	elif client.user in message.mentions:
		choice = random.choice([1,2])
		print(message.mentions)
		print("message : ", " ".join(message.content.split()[1:]))
		print(re.sub("<@!761886306049458207> ", "",message.content))
		response = chatbot.get_response(" ".join(re.sub("<@!761886306049458207>", "",message.content)))
		print("response : ",response)
		if(choice == 1):
			await message.channel.send(response) 
		else:
			await message.add_reaction('🇸')
			await message.add_reaction('🇹')
			await message.add_reaction('🇫')
			await message.add_reaction('🇺')
			response = random.choice(comebacks).strip()
			await message.channel.send("Hey "+str(message.author.mention)+", "+response) 
client.run(TOKEN)



