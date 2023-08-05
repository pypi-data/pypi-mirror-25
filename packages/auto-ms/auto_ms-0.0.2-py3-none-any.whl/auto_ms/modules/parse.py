from io import StringIO
import pandas as pd
import re
from collections import defaultdict
from pprint import pprint


def parse_file(file_path):
    regex = re.compile(r'\[(\w+)\]')
    parsed = defaultdict(list)
    cur = None
    with open(file_path) as f:
        for line in f:
            # skip comments
            if not line.strip() or line.startswith('#'):
                continue
            header = regex.findall(line)
            if header:
                cur = header[0].lower()
            else:
                parsed[cur].append(line.strip())
    return parsed

def parse_header(header_list):
    """
    reads header listdata, returns dictionary
    """
    # handle the different key depths
    keys = {'title': 1,
            'byapp': 1,
            'fileopentime': 1,
            'info': 2,
            'startupaxis': 2,
            'startupgroup': 2,
            'fieldgroup': 2,
            'plot_appearance': 1}

    res = defaultdict(dict)
    for line in header_list:
        #skip blanklines or comments
        if not line.strip() or line.startswith('#'):
            continue
        key, *data = line.strip().split(',')
        key = key.lower()
        if key not in keys:
            raise Exception('System not configured to handle key: {}'.format(key))
        length = keys[key]
        if length == 1:
            res[key] = data
        elif length == 2:
            res[key][data[0]] = data[1:]
    return res




def parse_data(data_list):
    fakefile = StringIO('\n'.join(data_list))
    return pd.read_csv(fakefile, sep=',', index_col=None)