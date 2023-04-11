import argparse
from os import walk
import os
parser = argparse.ArgumentParser()
parser.add_argument('--file_path')
args = parser.parse_args()
if args.file_path:
    print("===========================================")
    print(f'Trim data for {args.file_path}')
    print("===========================================")

source_file_path = r'datasets/MTL-Bioinformatics-2016-external-contexts/'+args.file_path

count = 0
for (_, _, filenames) in walk(source_file_path):
    for file_name in filenames:
        new_text = ''
        with open(os.path.join(source_file_path,file_name),'r',encoding='utf8') as f:
            text = f.read()
        sublists = text.strip().split('\n\n')
        tokens_block = []
        for item in sublists:
            tokens = item.split('\n')
            if len(tokens) >510:
                count+=1
                tokens = tokens[:509]
            new_text = '\n'.join(tokens)
            tokens_block.append(new_text)
        new_text = '\n\n'.join(tokens_block)
        print(count)
        with open(os.path.join(source_file_path,file_name),'w',encoding='utf8') as f:
            f.write(new_text)

