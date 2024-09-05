#File to read in prompts from batchinputs and extracts content from ChatGPT batch files

import os
import json
import re

path = 'input\\batchinputs'
files = []

#Put all inputs into files vector
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    print(filename)

    folder_name = None

    #Reading in output file
    with open(filepath, "r") as file:
        inputs = file.readlines()
    
        if re.match(r'raw_prompts2_[1-9]\.jsonl', filename):
            if not os.path.exists('input/prompts2'): 
                os.makedirs('input/prompts2')
            folder_name = 'input/prompts2'
        
        if folder_name == None: continue
        for input in inputs:
            # print('input: ', input)
            json_input = json.loads(input)

            #Extract the "custom id"
            id = json_input["custom_id"].replace("request-","")
            # print('id is: ', id)

            # Extract the "content" value
            content = json_input["response"]["body"]["choices"][0]["message"]["content"]
            # print('content:', content)
            file_path = os.path.join(folder_name, f'output{id}.txt')
            with open(file_path, 'w') as f:
                f.write(content)