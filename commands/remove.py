async def remove(item_to_remove, message, redis):
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