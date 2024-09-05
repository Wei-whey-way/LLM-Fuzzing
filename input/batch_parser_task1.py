#File to read in prompts from batchinputs and extracts content from ChatGPT batch files

import os
import json

path = 'input\\batchinputs'
files = []

#Put all inputs into files vector
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    # print(filename)

    #Reading in output file
    with open(filepath, "r") as file:
        inputs = file.readlines()

        match filename:
            # case 'raw_prompts1a.jsonl':
            #     if not os.path.exists('input/prompts1a'): os.makedirs('input/prompts1a')
            #     folder_name = 'input/prompts1a'
            
            # case 'v3_test3.5_raw_prompts1b_initial.jsonl':
            case 'raw_prompts1b_initial.jsonl':
                # print('1b')
                if not os.path.exists('input/prompts1b/initial'): os.makedirs('input/prompts1b/initial')
                folder_name = 'input/prompts1b/initial'
            
            case 'raw_prompts1b_handshake.jsonl':
                # print('1b')
                if not os.path.exists('input/prompts1b/handshake'): os.makedirs('input/prompts1b/handshake')
                folder_name = 'input/prompts1b/handshake'
            
            case 'raw_prompts1b_retry.jsonl':
                # print('1b')
                if not os.path.exists('input/prompts1b/retry'): os.makedirs('input/prompts1b/retry')
                folder_name = 'input/prompts1b/retry'
            
            case 'raw_prompts1b_versionnego.jsonl':
                # print('1b')
                if not os.path.exists('input/prompts1b/versionnego'): os.makedirs('input/prompts1b/versionnego')
                folder_name = 'input/prompts1b/versionnego'

            # case 'raw_prompts1b_.jsonl':
            #     # print('1b')
            #     if not os.path.exists('input/prompts1b/'): os.makedirs('input/prompts1b/')
            #     folder_name = 'input/prompts1b/'

            case 'raw_prompts2_test.jsonl':
                if not os.path.exists('input/prompts2'): os.makedirs('input/prompts2')
                folder_name = 'input/prompts2'

            case _:
                continue
        
        if folder_name == None: continue
        
        for i, input in enumerate(inputs):
            # print('input: ', input)
            json_input = json.loads(input)

            # Extract the "content" value
            content = json_input["response"]["body"]["choices"][0]["message"]["content"]
            # print('content:', content)
            file_path = os.path.join(folder_name, f'output{i+1}.txt')
            with open(file_path, 'w') as f:
                f.write(content)

#Function to clean up versionnego folder
versionnegopath = 'input/prompts1b/versionnego'
for filename in os.listdir(versionnegopath):
    filename = versionnegopath + "/" + filename
    with open(filename, 'r') as file:
        lines = file.readlines()

    result = []
    inside_supported_version = False
    combined_line = ""

    for line in lines:
        stripped_line = line.strip()
        # print('stripped line: ', stripped_line)

        # Check if the line contains 'Supported Version (32)'
        if "Supported Version (32)" in stripped_line:
            # If it already contains both '[' and ']', skip
            if '[' in stripped_line and ']' in stripped_line:
                # print(stripped_line, ' already contains both brackets')
                continue

            # If inside the Supported Version array and '[' was found but ']' is not yet found
            if '[' in stripped_line and ']' not in stripped_line:
                inside_supported_version = True
                # combined_line = "["
                # print('uh oh: ', stripped_line)

        
        if inside_supported_version:
            # print('aaaa', stripped_line)
            combined_line += " " + stripped_line
            if ']' in stripped_line:
                combined_line = combined_line.replace("[","").replace("]","").strip()
                # print('appending: ', combined_line)
                result.append(combined_line)
                inside_supported_version = False
                combined_line = ""
            continue

        # If not inside Supported Version array, just add the line as is
        result.append(stripped_line)
    
    print('final result: ', result, '\n')

    # Write the result back to the file or print it
    with open(filename, 'w') as file:
        for line in result:
            file.write(line + "\n")