# For each fold in the 'train' and 'test' folders, we load question.txt, metadata.json, and input_output.json
# and create a new file combining all the information in a single json file.

import json
import os
import sys

def main(target='./train'):
    # Loop through all the folders
    for fold in os.listdir(target):
        fold_path = os.path.join(target, fold)
        try:
            if os.path.isdir(fold_path):
                # Load the data from the files
                question = open(os.path.join(fold_path, 'question.txt')).read()
                metadata = json.load(open(os.path.join(fold_path, 'metadata.json')))
                input_output = json.load(open(os.path.join(fold_path, 'input_output.json')))
                # Create a new dictionary with the data
                data = {
                    'question': question,
                    'metadata': metadata,
                    'input_output': input_output
                }
                # Save the data to a new file
                with open(os.path.join(fold_path, 'data.json'), 'w') as f:
                    json.dump(data, f, indent=2)
        except:
            print('Error in folder: {}'.format(fold_path))

if __name__ == '__main__':
    main()