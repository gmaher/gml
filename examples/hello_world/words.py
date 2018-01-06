import sys
import os
sys.path.append(os.path.abspath('../..'))
from graph import Graph

words_1 = ['hello', 'what\'s', 'dictionary']
words_2 = ['world', 'up', 'object']
ids     = [2,0,1]

g = Graph()

w1 = lambda x: words_1[x]
w2 = lambda x: words_2[x]
merge   = lambda x,y: " ".join([x,y])
count   = lambda x: len(x)
repeat = lambda x,y: " ".join([y]*x)

g.add_node(name='id')
g.add_node(w1, 'word_1', depends=['id'])
g.add_node(w2, 'word_2', depends=['id'])
g.add_node(merge, 'merge', depends=['word_1', 'word_2'])
g.add_node(count, 'count', depends=['word_1'])
g.add_node(repeat, 'repeat', depends=['count','merge'])

out = lambda x: g.get('repeat',{'id':x})

answer = [out(x) for x in ids]
print answer
