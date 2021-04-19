import os
import json

#Discord Connections
import discord
from dotenv import load_dotenv

#Webscraping
import datetime
import srcomapi, srcomapi.datatypes as dt
api = srcomapi.SpeedrunCom(); api.debug = 1

# with open('strats.json') as f:
#     strat_json = json.load(f)

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
    
    #Help
    if message.content == '!help':
        await message.channel.send('**HELP**:\n- !wr [Category]\n- !role [role name]\n- !strats [area] [strat name]')

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
    
    #Bot Introduction
    if message.content == '!intro':
        await message.channel.send('Hello, I\'m Balan Speedybot and I\'m here to help. I can give you roles and tell you world records and strats. Use the commands **!role**, **!wr** and **!strats** and I can help you out!\n\nUse **!help** for instrctions on using the commands and keep the majority of my use in #bot-spam')

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
    
    #Show Strats
    if message.content.startswith('!strats'):
        with open('strats.json') as f:
            strat_json = json.load(f)
        
        commands = message.content.replace('!strats', '')
        commands = commands.strip()

        level_keys = []
        for i in strat_json['Strats'].keys():
            level_keys.append(i)

        if commands == '':
            response = 'Available Areas For Strats:\n'
            for i in level_keys:
                response += f'- {i}\n'
        elif commands == level_keys[0]:
            response = strat_json['Strats'][commands]
        elif any(commands.startswith(s) for s in level_keys):
            if commands in level_keys:
                response = 'Available strats in this area:\n'
                for strat in strat_json['Strats'][commands]:
                    response += f'- {strat}\n'
            else:
                commands = commands.split(" ", 1)
                try:
                    response = f'{commands[1]}:\n'
                    response += strat_json['Strats'][commands[0]][commands[1]]
                except:
                    response = 'Please enter a valid strat'
        else:
            response = 'Please put in a valid area of strats'

        await message.channel.send(response)

@client.event
async def on_user_update(before, after):
    print(before)
    print(after)

client.run(TOKEN)
