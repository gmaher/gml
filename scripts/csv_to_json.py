import argparse
import os
import ast
from tqdm import tqdm
import json

# def get_type(input_data):
#     try:
#         return type(literal_eval(input_data))
#     except (ValueError, SyntaxError):
#         # A string, so return str
#         return str

def get_val(input_data):
    try:
        return ast.literal_eval(input_data)
    except:
        return str(input_data)

parser  = argparse.ArgumentParser()
parser.add_argument('-input_file')
parser.add_argument('-output_dir')
parser.add_argument('--N', default=1000000, type=int)
args = parser.parse_args()

N = args.N

input_file = os.path.abspath(args.input_file)
csv_file   = open(input_file, 'r')

output_dir = os.path.abspath(args.output_dir)

#get columns in first line
cols = csv_file.readline().split(',')

for i in tqdm(range(N)):
    line = csv_file.readline().replace('\n','')
    vals = line.split(',')
    vals = [get_val(v) for v in vals]

    d = {}
    for k,v in zip(cols,vals): d[k] = v

    with open(output_dir+'/{}.json'.format(i), 'w') as f:
        json.dump(d,f, indent=2, sort_keys=True)
