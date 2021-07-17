import discord
import os
from dotenv import load_dotenv
from random import randrange
import redis

from commands.keep import keep
from commands.responses import response_to_boblin
from commands.show import show
from commands.remove import remove

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
            await show(item_to_show, message, redis)
        
        # REMOVE COMMAND
        if boblin_command.startswith('remove'):
            item_to_remove = boblin_command[7:].strip()
            await remove(item_to_remove, message, redis)
                
client.run(os.getenv('TOKEN'))
    