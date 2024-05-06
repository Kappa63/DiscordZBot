import numpy as np
import matplotlib.pyplot as plt
import math

reels = 3
window = 3
payline = window//2
price = 25
divisor = 0.2

sym = {"cherry":0, "watermelon":0, "lemon":0, "chocolate":0, "bell":0, "seven":0}

reel_weights = [[0.35, 0.25, 0.2, 0.14, 0.045, 0.015], 
                [0.4, 0.2, 0.24, 0.1, 0.0475, 0.0125], 
                [0.3, 0.3, 0.245, 0.1, 0.025, 0.03]]
matches = []
iters = 100000

def calcMultiplier2(mults:float):
    return round(divisor/(math.prod(mults)), 2)

def getWeight(reel, symbl):
        return reel_weights[reel%3][list(sym).index(symbl)]

for _ in range(iters):
    m = []
    for i in range(reels):
        c = np.random.choice(list(sym.keys()), size=window, p=reel_weights[i])
        m.append(c[payline])
    matches.append(m)

for i in matches:
    if len(set(i)) == 1:
        sym[i[0]] += 1

plt.bar(sym.keys(), sym.values())
for i, v in enumerate(sym.values()):
    plt.text(i-0.1, v+0.05, str(v))

spent = price*iters
money = 0
for k,v in sym.items():
    mult = calcMultiplier2([getWeight(i, k) for i in range(reels)])
    match k:
        case "cherry":
            money += mult*price*v
        case "watermelon":
            money += mult*price*v
        case "lemon":
            money += mult*price*v
        case "chocolate":
            money += mult*price*v
        case "bell":
            money += mult*price*v
        case "seven":
            money += mult*price*v
print(f"spent: {spent:,}$\nwins: {money:,}$\nprofit: {(money-spent):,}$")
 
plt.xlabel('Symbol')
plt.ylabel('Wins')
plt.title(f'ZBot Slots Wins Over {iters:,} Spins')
 
plt.show()