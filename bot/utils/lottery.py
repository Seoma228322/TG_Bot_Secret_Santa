import random

def loterry(users):
    random.shuffle(users)
    pairs = []
    for i in range(len(users)):
        giver = users[i]
        recipient = users[(i + 1) % len(users)]
        pairs.append((giver, recipient))
    
    return pairs