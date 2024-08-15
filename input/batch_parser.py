import os
import json

path = 'input\\batchinputs'
files = []

#Put all inputs into files vector
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    print(filename)

    #Reading in output file
    with open(filepath, "r") as file:
        inputs = file.readlines()

        match filename:
            case 'raw_prompts1a.jsonl':
                if not os.path.exists('input/prompts1a'): os.makedirs('input/prompts1a')
                folder_name = 'input/prompts1a'

        # if folder_name == None:
        
        for i, input in enumerate(inputs):
            json_input = json.loads(input)

            # Extract the "content" value
            content = json_input["response"]["body"]["choices"][0]["message"]["content"]
            file_path = os.path.join(folder_name, f'output{i+1}.txt')
            with open(file_path, 'w') as f:
                f.write(content)

        
