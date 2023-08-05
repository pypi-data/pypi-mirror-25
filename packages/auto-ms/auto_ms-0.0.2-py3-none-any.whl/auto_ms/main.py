import os
from auto_ms.modules import parse, process
from pprint import pprint
from collections import defaultdict
import argparse

def tempsplit_entry():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", type=str, help="MS data file to split by temperature")
    parser.add_argument("outdir", type=str, help="Output directory")
    args = parser.parse_args()
    tempsplit(args.data_file, args.outdir)


def tempsplit(target_path, outdir):
    parsed = parse.parse_file(target_path)
    header = parse.parse_header(parsed['header'])
    data = parse.parse_data(parsed['data'])
    split_data = process.split_data(data)

    # write the output
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(os.path.join(outdir, 'tsvs')):
        os.makedirs(os.path.join(outdir, 'tsvs'))
    for temp, df in split_data.items():
        print('Processing temperature: {}'.format(temp))
        df = df[['Field (Oe)', 'Temperature (K)', "m' (emu)", 'm\" (emu)', 'Wave Frequency (Hz)']]
        df.to_csv(os.path.join(outdir, 'tsvs', "T{}.tsv".format(temp)), 
                  sep="\t",
                  index=None,
                  quoting=3)
    print("Completed")
    return 0




def execute(target_path, out_path):
    parsed = parse.parse_file(target_path)
    header = parse.parse_header(parsed['header'])
    data = parse.parse_data(parsed['data'])
    split_data = process.split_data(data)

    # write the output
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    if not os.path.exists(os.path.join(out_path, 'tsvs')):
        os.makedirs(os.path.join(out_path, 'tsvs'))
    for temp, df in split_data.items():
        df = df[['Field (Oe)', 'Temperature (K)', "m' (emu)", 'm\" (emu)', 'Wave Frequency (Hz)']]
        df = process.calculate_chi(df, 51.2, 0, 1.80573e-05, -0.00049552)
        print(df.columns)
        df.to_csv(os.path.join(out_path, 'tsvs', "T{}.tsv".format(temp)), 
                  sep="\t",
                  index=None,
                  quoting=3)

if __name__ == '__main__':

    execute('testdata/ErCOTTHFBPh4-ac-vartemp-1750Oe.ac.dat', 'output/testout')