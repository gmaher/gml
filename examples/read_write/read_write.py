import sys
import os
sys.path.append(os.path.abspath('../..'))
from graph import Graph

read = lambda x: open(x,'r').read()

class CountWriter:
    def __init__(self):
        self.count = 0
    def write(self,x):
        with open('./words_3/{}.txt'.format(self.count),'w') as f:
            f.write(x)
        self.count += 1

merge = lambda x,y: " ".join([x,y])
write = CountWriter()


g = Graph()

g.add_node(name='words_1')
g.add_node(name='words_2')
g.add_node(read, 'reads_1', depends=['words_1'])
g.add_node(read, 'reads_2', depends=['words_2'])
g.add_node(merge,'merge',depends=['reads_1','reads_2'])
g.add_node(write.write, 'words_3', depends=['merge'])

words_1 = ['./words_1/'+w for w in os.listdir('./words_1')]
words_2 = ['./words_2/'+w for w in os.listdir('./words_2')]

for x,y in zip(words_1,words_2):
    g.get('words_3',{'words_1':x, 'words_2':y})
