import yaml
import csv
import json
import os


def mkdir(fn):
  if not os.path.exists(os.path.abspath(fn)):
    try:
      os.mkdir(os.path.abspath(fn))
    except:
      pass

def upsert_dirs(dirpath):
  """
  Similar to os.makedirs, but doesn't raise an error when
  a directory is already in existence...it just skips it.

  :param str dirpath: Directory path to upsert all directories in
  """
  # Get only the dir names
  dirs = [d for d in dirpath.split('/') if d]

  if dirpath.startswith('/'):
    path = '/'
  else:
    path = ''

  for d in dirs:
    path += (d + '/')

    if not os.path.exists(path):
      try:
        os.mkdir(path)
      except:
        pass

def configure_dirs(base_dir, config):
  for key in config['DIR_KEYS']:
    # Convert dirs to absolute dirs
    config[key] = os.path.join(base_dir, config[key])

    # Upsert dirs recursively
    #upsert_dirs(config[key])

  return config

def load_yaml(fn):
  """loads a yaml file into a dict"""
  with open(fn, 'r') as file_:
    try:
      return yaml.load(file_)
    except RuntimeError as e:
      print('failed to load yaml fille {}, {}\n'.format(fn, e))

def save_yaml(fn, data):
  with open(fn, 'w') as file_:
    yaml.dump(data, file_, default_flow_style=False)

def save_csv(filename, dict):
  with open(filename, 'w') as f:
    w = csv.DictWriter(f, dict.keys())
    w.writeheader()
    w.writerow(dict)

def load_csv(filename):
  with open(filename, 'r') as f:
    w = csv.DictReader(f)
    d = [row for row in w]
    if len(d) == 1:
      return d[0]
    else:
      return d

def load_json(fn):
  with open(fn) as f:
    return json.load(f)

def save_json(fn, data):
  with open(fn, 'w') as outfile:
    json.dump(data, outfile, indent=2, sort_keys=True)
