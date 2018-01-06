import sys
import os
sys.path.append(os.path.abspath('../..'))
from graph import Graph
"""
Here we make the graph

A   B
 \ /
  D =(A+B)
  |
  |         C
  |         |
  --------- E = (D*C)
"""
numbers_1 = [1,2,3,4]
numbers_2 = [1,1,1,1]
numbers_3 = [2,2,2,2]
numbers_4 = [4,4,4,4]
plus = lambda x,y: x+y
mult = lambda x,y: x*y

g = Graph()
g.add_node(name='A')
g.add_node(name='B')
g.add_node(name='C')

g.add_node(plus,name='D',depends=['A','B'])
g.add_node(mult,name='E',depends=['D','C'])

out = lambda x,y,z: g.get('E',input_dict={'A':x,'B':y,'C':z})

answer   = [out(x,y,z) for x,y,z in zip(numbers_1,numbers_2,numbers_3)]
answer_2 = [out(x,y,z) for x,y,z in zip(numbers_1,numbers_2,numbers_4)]
print answer
print answer_2
