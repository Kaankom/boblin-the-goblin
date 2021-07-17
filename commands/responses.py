import time
from random import randrange


words = ['yes', 'what', 'yeah', 'what can humble boblin do for you', 'hmm', 'ya', 'yeah, what', 'WHAT']
grants = ['sigh...', '...', 'ohh god, leave me al...', 'go die...', 'stupid, stinky fu...', 'I hope you die...', '...']

def get_word():
    return words[randrange(0, len(words))]

def get_grant():
    return grants[randrange(0, len(grants))]

async def response_to_boblin(message):
    await message.channel.send('...')
    time.sleep(0.8)
    await message.channel.send('...')
    time.sleep(0.8)
    await message.channel.send(f'*{get_grant()}*')
    time.sleep(0.3)
    await message.channel.send(f'{get_word()}?')