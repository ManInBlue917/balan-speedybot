import os

#Discord Connections
import discord
from dotenv import load_dotenv

#Webscraping
import datetime
import srcomapi, srcomapi.datatypes as dt
api = srcomapi.SpeedrunCom(); api.debug = 1

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('SERVER_NAME')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=SERVER)

    print(
        f'{client.user} has connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #view WRs
    if message.content.startswith('!wr'):
        src_game = api.search(dt.Game, {"name": "balan wonderworld"})[0]

        message_commands = message.content.replace('!wr', '')
        message_commands = message_commands.strip()

        cat_list = []
        for category in src_game.categories:
            cat_list.append(category.name)

        if message_commands == '':
            response = 'Current Categories:\n'
            for cat in cat_list:
                response += f'- {cat}\n'
        else:
            try:
                cat_index = cat_list.index(message_commands)

                if len(src_game.categories[cat_index].records[0].runs) == 0:
                    response = 'There are no runs for this category'
                else:
                    record_user = src_game.categories[cat_index].records[0].runs[0]["run"].players[0].names["international"]
                    record_time = src_game.categories[cat_index].records[0].runs[0]["run"].times["primary_t"]

                    record = [record_user, str(datetime.timedelta(seconds=record_time))]
                    response = f'The {src_game.categories[cat_index].name} record is {record[1]} by {record[0]}'
            except:
                response = 'Please use the correct input'

        await message.channel.send(response)
    
    #self assign roles
    if message.content.startswith('!role'):
        commands = message.content.replace('!role', '')
        commands = commands.strip()

        if commands == '': #Print list of available roles
            roles_to_print = []
            for role in client.guilds[0].roles:
                if role.name == "Balan Speedybot":
                    break
                else:
                    roles_to_print.append(role.name)
            
            response = f'Available roles:\n'
            for i in roles_to_print[1:]:
                response += f'- {i}\n'
            
            await message.channel.send(response)
        else: #look for and add role to user
            role_to_add = None
            for role in client.guilds[0].roles:
                if role.name == commands:
                    role_to_add = role
                    break

            if role_to_add != None:
                if role_to_add in message.author.roles:
                    await message.author.remove_roles(role_to_add)
                    await message.channel.send('Role Removed!')
                else:
                    await message.author.add_roles(role_to_add)
                    await message.channel.send('Role Added!')
            else:
                await message.channel.send('Please Input A Valid Role.')

client.run(TOKEN)
