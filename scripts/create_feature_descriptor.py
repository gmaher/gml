import os
import json
import argparse
import pandas as pd
from tqdm import tqdm

from dateutil.parser import parse

def is_date_func(string):
    try:
        parse(string)
        return True
    except:
        return False

parser = argparse.ArgumentParser()
parser.add_argument('-input')
parser.add_argument('-output_dir')
# parser.add_argument('-override_file')
parser.add_argument('-max_int_categories', type=int)

args = parser.parse_args()

input_ = os.path.abspath(args.input)

files = os.listdir(input_)
files = [input_ + '/' + f for f in files]

# override_file = os.path.abspath(args.override_file)
# with open(override_file,'r') as f:
#     override = json.load(f)

feature_names = {}
for f in tqdm(files):
    with open(f,'r') as record:
        r = json.load(record)

        for k in r.keys(): feature_names[k] = 1

features    = {}
descriptors = {}

for k in feature_names.keys():
    features[k] = []
    print(k)
    for f in tqdm(files):
        with open(f,'r') as record:
            r = json.load(record)

            if k in r: features[k].append(r[k])

    vals = list(set(features[k]))
    is_float  = any([type(v) == float for v in vals])
    is_string = any([type(v) == str for v in vals if not v == ""])
    is_int    = any([type(v) == int for v in vals])
    is_date   = any([is_date_func(v) for v in vals])

    if is_date:
        descriptors[k] = {"type":"date"}
    elif is_string:
        descriptors[k] = {"type":"categorical", "values":vals}
    elif is_float:
        descriptors[k] = {"type":"number"}
    elif is_int:
        if len(vals) <= args.max_int_categories:
            descriptors[k] = {"type":"categorical", "values":vals}
        else:
            descriptors[k] = {"type":"number"}
    else:
        print("could not recognize feature {}".format(k))

with open(args.output_dir+'/feature_descriptor.json','w') as f:
    json.dump(descriptors, f, indent=2, sort_keys=True)
