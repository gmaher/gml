import json
import random

words = ['banana', 'apple', 'eggplant', 'orange', 'avacado']

for i in range(50):
    w1 = random.sample(words, 1)[0]
    w2 = random.sample(words, 1)[0]

    with open('./words_1/{}.txt'.format(i), 'w') as f:
        f.write(w1)


    with open('./words_2/{}.txt'.format(i), 'w') as f:
        f.write(w2)
