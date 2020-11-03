import random

def Bones():
    return random.choice(range(1,6))
def PureG():
    return random.choice(range(1,10))
def Dirt():
    return random.choice(range(10,15))
def Copper():
    return random.choice(range(5,9))
def Landmine():
    return random.choice(range(1,2))
def Plumbing():
    return random.choice(range(1,2))
def Item(key):
    choices = {'Bones': Bones(), 'Pure Gold': PureG(),"Dirt": Dirt(),"Copper": Copper(),"Landmine": Landmine(),"Plumbing": Plumbing()}
    return choices.get(key, 'default')
