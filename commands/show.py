import discord

async def show(item_to_show, message, redis):
    if item_to_show == 'all':
        keys = redis.keys(f'{message.author}:*')
        if len(keys) > 0:
            embed = discord.Embed(title = f'{message.author}\'s storage', description = 'Items', color = 0xd9b99b)
            for key in keys:
                embed.add_field(name = 'Item', value = redis.get(key).decode('utf-8').capitalize(), inline = True )
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('There is nothing on me you poor bastard')
                    
    if item_to_show != 'all':        
        if redis.exists(f'{message.author}:{item_to_show}'):
            await message.channel.send(f'Here you go: {item_to_show}')
        else:
            await message.channel.send(f'I don\'t have no {item_to_show}')