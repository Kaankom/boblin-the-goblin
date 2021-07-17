from random import randrange

items = []

greetings = ['Allright', 'Ok', 'Well, ok then', 'Ok, ok', 'Fine...', 'Right then', 'Yeah... aha']

desriptions = ['stupid', 'useless', 'impractical', 'unusable', 'bloody', 'worthless', 'scrappy', 'good-for-nothing', 'nonfunctional', 'rotten', 'cheesy', 'piss-poor', 'creepy']

actions = ['I will store your', 'I will keep your', 'I\'ll have your', 'give me your']

# get random greeting
def get_greeting():
    return greetings[randrange(0, len(greetings))]

def get_description():
    return desriptions[randrange(0, len(desriptions))]

def get_action():
    return actions[randrange(0, len(actions))]

async def keep(boblin_command, redis, message):
    item_to_store = boblin_command[5:].strip()
    #items.append(item_to_store)
    redis.set(f'{message.author}:{item_to_store}', item_to_store)
    await message.channel.send(f'{get_greeting()}, {get_action()} {get_description()} {item_to_store.capitalize()}')
    