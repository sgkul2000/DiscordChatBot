import requests, os, random
import discord


cwd = os.getcwd()  # Get the current working directory (cwd)

with open(cwd+"/static/comebacks.txt","r") as comebacksFile:
	comebacks = list(comebacksFile)

def getInsult():
	response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
	return response.json()['insult']

def getCompliment():
	response = requests.get("https://complimentr.com/api")
	return response.json()['compliment']
# 
def getJoke():
	response = requests.get("https://sv443.net/jokeapi/v2/joke/Any")
	if(response.json()['type'] == "twopart"):
		print([response.json()['setup'], response.json()['delivery']])
		return [response.json()['setup'], response.json()['delivery']]
	else:
		return response.json()['joke']


botHelp = 'Hey, i am an **interactive insult bot**. Feel free to abuse others and yourself with the following commands.\nBot Commands: \n- **!insult**: Insult a random person on the server\n- **!insult <name>**: Insults person with name <name>.\n- **!insult me**: Insults you\n- **!insult yourself**: Insults itself\n- **!joke**:Cracks a joke\nOptionally all commands accept a "tts" parameter at the end. this results in a text to speech insult'


def getCommandResponse(msg, message, client):
	if msg.startswith('!help'):
		response = discord.Embed(title="Insult Help", color=0x2196F3)
		response.description = botHelp
	elif msg.startswith('!insult'):
		insultToSend = getInsult()
		name = ''
		if ' ' in msg:
			name = msg.split()[1]
		if len(name)>0:
			if name != 'me':
				response = "Hey "+name+", "+insultToSend
			if name == 'me':
				response = "Hey <@"+str(message.author.id)+">, "+insultToSend
			if name == 'yourself':
				# response = "Hey Insult Bot, "+insultToSend
				response = "Hey <@"+str(client.user.id)+">, "+insultToSend
		else:
			members = message.guild.members
			memberList = []
			for member in members:
				if not member.bot:
					memberList.append(member.id)
			person = random.choice(memberList)
			response = "Hey <@"+str(person)+">, "+insultToSend
		return response
	
	elif msg.startswith('!joke'):
		response = getJoke()
	elif msg.startswith("!compliment"):
		complimentToSend = getCompliment()
		name = ''
		if ' ' in msg:
			name = msg.split()[1]
		if len(name)>0:
			if name != 'me':
				response = "Hey "+name+", "+complimentToSend
			if name == 'me':
				response = "Hey <@"+str(message.author.id)+">, "+complimentToSend
			if name == 'yourself':
				response = "Hey <@"+str(client.user.id)+">, "+complimentToSend
		else:
			person = random.choice(list(member.id for member in message.guild.members if not member.bot))
			response = "Hey <@"+str(person)+">, "+complimentToSend
	elif msg.startswith("!comeback"):
		comeback = random.choice(comebacks)
		name = ''
		if ' ' in msg:
			name = msg.split()[1]
		if len(name)>0:
			if name != 'me':
				response = "Hey "+name+", "+comeback
			if name == 'me':
				response = "Hey <@"+str(message.author.id)+">, "+comeback
			if name == 'yourself':
				response = "Hey <@"+str(client.user.id)+">, "+comeback
	else:
		# response = "Invalid Command. Please type '!insult help' for a list of commands"
		response = discord.Embed(title="Invalid command. try one of these", color=0x2196F3)
		response.description = botHelp
		
	return response