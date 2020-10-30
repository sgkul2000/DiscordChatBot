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

intents = discord.Intents().all()
client = discord.Client(intents=intents)

chatbot = ChatBot('Roden')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")
print('training done')


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
    if msg.startswith('!amongus'):
        # sentMessage = await message.channel.send("helloworld")
        sentMessage = await message.channel.send(embed=discord.Embed(title="Among us mode.", description="Code: ABCDEF\nServer: Asia", color=0xFF8008))
        await sentMessage.add_reaction('⏹️')
        await sentMessage.add_reaction('▶️')
        await sentMessage.add_reaction('🔊')
    elif msg.startswith('!'):
        response = getCommandResponse(msg, message, client)
        await message.delete()
        if(type(response) == discord.Embed):

            newmessage = await message.channel.send(embed=response)
            await newmessage.delete(delay=20)
        elif type(response) == list:
            await message.channel.send(response[0], tts=tts)
            await message.channel.send(response[1], tts=tts)
        else:
            await message.channel.send(html.unescape(response), tts=tts)
    elif client.user in message.mentions:
        choice = random.choice([1, 2])
        print(message.mentions)
        print("message : ", " ".join(message.content.split()[1:]))
        print(re.sub("<@!761886306049458207> ", "", message.content))
        response = chatbot.get_response(
            re.sub("<@!761886306049458207>", "", message.content))
        print("response : ", response)
        if(choice == 1):
            await message.channel.send(response)
        else:
            await message.add_reaction('🇸')
            await message.add_reaction('🇹')
            await message.add_reaction('🇫')
            await message.add_reaction('🇺')
            response = random.choice(comebacks).strip()
            await message.channel.send("Hey "+str(message.author.mention)+", "+response)


@client.event
async def on_raw_reaction_add(payload):
    # check message logic
    message = await payload.member.guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.member != client.user and message.author == client.user and message.embeds[0].title == "Among us mode.":
        # check channel logic
        if payload.member.voice == None:
            await payload.member.guild.get_channel(payload.channel_id).send(
                "<@{}>, You are not in a voice channel right now. Please join one before trying again.".format(payload.member.id))
        else:
            if payload.emoji.name == "⏹️":
                # mute members logic
                for member in payload.member.voice.channel.members:
                    await member.edit(mute=True)
            elif payload.emoji.name == "🔊":
                code = re.findall(
                    "Code: ([A-z]+)", message.embeds[0].description)
                server = re.findall(
                    "Server: ([a-zA-Z]+)", message.embeds[0].description)
                await payload.member.guild.get_channel(payload.channel_id).send(
                    "Among us:\nCode: {}\nServer: {}".format(code[0], server[0]), tts=True)


@client.event
async def on_raw_reaction_remove(payload):
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    print(member.status)
    channelList = await guild.fetch_channels()
    for chnl in channelList:
        if(chnl.id == payload.channel_id):
            channel = chnl
            message = await chnl.fetch_message(payload.message_id)

    # check message logic
    # message = await payload.member.guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.user_id != client.user.id and message.author == client.user and message.embeds[0].title == "Among us mode.":
        # check channel logic
        member = await guild.fetch_member(payload.user_id)
        if member.voice == None:
            await channel.send(
                "<@{}>, You are not in a voice channel right now. Please join one before trying again.".format(member.id))
        else:
            if payload.emoji.name == "⏹️":
                # unmute members logic
                for mem in member.voice.channel.members:
                    await mem.edit(mute=False)


client.run(TOKEN)
