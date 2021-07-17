import discord
import os
from dotenv import load_dotenv
from random import randrange
import redis

from commands.keep import keep
from commands.responses import response_to_boblin

load_dotenv()

redis = redis.Redis(host = 'localhost', port = os.getenv('REDIS_PORT'))

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    message.content = message.content.lower()
    
    if message.content.startswith('boblin'):
        
        boblin_command = message.content[7:].strip()
        
        # HELP
        if boblin_command == 'help':
            embed =  discord.Embed(title = 'HELP', description = 'Boblin Commands', color = 0x7d95b9)
            embed.add_field(name = 'KEEP', value = 'Command: boblin keep <ITEM>', inline = True)
            embed.add_field(name = 'SHOW ITEM', value = 'Command: boblin show <ITEM>', inline = True)
            embed.add_field(name = 'SHOW ALL', value = 'Command: boblin show all', inline = True)
            embed.add_field(name = 'REMOVE ITEM', value = 'Command: boblin remove <ITEM>', inline = True)
            embed.add_field(name = 'REMOVE ALL', value = 'Command: boblin remove all', inline = True)
            await message.channel.send(embed=embed)

            
        # RESPONSES TO "boblin"
        if boblin_command == '':
            await response_to_boblin(message)
        
        # KEEP COMMAND
        if boblin_command.startswith('keep'):
            await keep(boblin_command, redis, message)
            
        # SHOW COMMAND
        if boblin_command.startswith('show'):
                        
            item_to_show = boblin_command[5:].strip()
            
            if item_to_show == 'all':
                keys = redis.keys(f'{message.author}:*')
                if len(keys) > 0:
                    embed = discord.Embed(title = f'{message.author}\'s storage', description = 'description', color = 0xd9b99b)
                    for key in keys:
                        embed.add_field(name = 'Item', value = redis.get(key).decode('utf-8'), inline = True )
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send('There is nothing on me you poor bastard')
                    
            if item_to_show != 'all':        
                if redis.exists(f'{message.author}:{item_to_show}'):
                    await message.channel.send(f'Here you go: {item_to_show}')
                else:
                    await message.channel.send(f'I don\'t have no {item_to_show}')
        
        # REMOVE COMMAND
        if boblin_command.startswith('remove'):
            item_to_remove = boblin_command[7:].strip()
            if item_to_remove == 'all':
                keys = redis.keys(f'{message.author}:*')
                if len(keys) > 0:
                    for key in keys:
                        print(key.decode('utf-8'))
                        redis.delete(key.decode('utf-8'))
                    await message.channel.send('Okay. I\'ll remove all your junk')
                else:
                    await message.channel.send('You don\'t have anything I could remove.')
                    
            if item_to_remove != 'all':    
                if redis.exists(f'{message.author}:{item_to_remove}'):
                    redis.delete(f'{message.author}:{item_to_remove}')
                    await message.channel.send('aaaand... it\'s gone.')
                
client.run(os.getenv('TOKEN'))
    