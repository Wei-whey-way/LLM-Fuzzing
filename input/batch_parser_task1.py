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
            #     if not os.path.exists('input/prompts1a/all'): os.makedirs('input/prompts1a/all')
            #     folder_name = 'input/prompts1a/all'
            
            # case 'raw_prompts1a-chatafl.jsonl':
            #     if not os.path.exists('input/prompts1a/chatafl'): os.makedirs('input/prompts1a/chatafl')
            #     folder_name = 'input/prompts1a/chatafl'
            
            # case 'raw_prompts1a-rag.jsonl':
            #     if not os.path.exists('input/prompts1a/rag'): os.makedirs('input/prompts1a/rag')
            #     folder_name = 'input/prompts1a/rag'
            
            # case 'raw_prompts1a-context.jsonl':
            #     if not os.path.exists('input/prompts1a/context'): os.makedirs('input/prompts1a/context')
            #     folder_name = 'input/prompts1a/context'
            
            # case 'raw_prompts1b_initial-all.jsonl':
            #     # print('1b')
            #     if not os.path.exists('input/prompts1b/initial/all'): os.makedirs('input/prompts1b/initial/all')
            #     folder_name = 'input/prompts1b/initial/all'
            
            # case 'raw_prompts1b_initial-template.jsonl':
            #     if not os.path.exists('input/prompts1b/initial/template'): os.makedirs('input/prompts1b/initial/template')
            #     folder_name = 'input/prompts1b/initial/template'

            # case 'raw_prompts1b_initial-rag.jsonl':
            #     if not os.path.exists('input/prompts1b/initial/rag'): os.makedirs('input/prompts1b/initial/rag')
            #     folder_name = 'input/prompts1b/initial/rag'
            
            # case 'raw_prompts1b_handshake-all.jsonl':
            #     if not os.path.exists('input/prompts1b/handshake/all'): os.makedirs('input/prompts1b/handshake/all')
            #     folder_name = 'input/prompts1b/handshake/all'
            
            # case 'raw_prompts1b_handshake-template.jsonl':
            #     if not os.path.exists('input/prompts1b/handshake/template'): os.makedirs('input/prompts1b/handshake/template')
            #     folder_name = 'input/prompts1b/handshake/template'
            
            # case 'raw_prompts1b_retry-all.jsonl':
            #     if not os.path.exists('input/prompts1b/retry/all'): os.makedirs('input/prompts1b/retry/all')
            #     folder_name = 'input/prompts1b/retry/all'
            
            # case 'raw_prompts1b_retry-template.jsonl':
            #     if not os.path.exists('input/prompts1b/retry/template'): os.makedirs('input/prompts1b/retry/template')
            #     folder_name = 'input/prompts1b/retry/template'
            
            # case 'raw_prompts1b_versionnego-all.jsonl':
            #     # print('1b')
            #     if not os.path.exists('input/prompts1b/versionnego/all'): os.makedirs('input/prompts1b/versionnego/all')
            #     folder_name = 'input/prompts1b/versionnego/all'

            # case 'raw_prompts1b_versionnego-template.jsonl':
            #     # print('1b')
            #     if not os.path.exists('input/prompts1b/versionnego/template'): os.makedirs('input/prompts1b/versionnego/template')
            #     folder_name = 'input/prompts1b/versionnego/template'

            # case 'raw_prompts1b_0rtt-all.jsonl':
            #     if not os.path.exists('input/prompts1b/0rtt/all'): os.makedirs('input/prompts1b/0rtt/all')
            #     folder_name = 'input/prompts1b/0rtt/all'

            case 'raw_prompts1b_0rtt-rag.jsonl':
                if not os.path.exists('input/prompts1b/0rtt/rag'): os.makedirs('input/prompts1b/0rtt/rag')
                folder_name = 'input/prompts1b/0rtt/rag'
            
            # case 'raw_prompts1b_0rtt-template.jsonl':
            #     if not os.path.exists('input/prompts1b/0rtt/template'): os.makedirs('input/prompts1b/0rtt/template')
            #     folder_name = 'input/prompts1b/0rtt/template'

            # case 'raw_prompts1b_1rtt-all.jsonl':
            #     if not os.path.exists('input/prompts1b/1rtt/all'): os.makedirs('input/prompts1b/1rtt/all')
            #     folder_name = 'input/prompts1b/1rtt/all'
            
            # case 'raw_prompts1b_1rtt-template.jsonl':
            #     if not os.path.exists('input/prompts1b/1rtt/template'): os.makedirs('input/prompts1b/1rtt/template')
            #     folder_name = 'input/prompts1b/1rtt/template'

            # case 'raw_prompts1b_1rtt-template.jsonl':
            #     if not os.path.exists('input/prompts1b/1rtt/template'): os.makedirs('input/prompts1b/1rtt/template')
            #     folder_name = 'input/prompts1b/1rtt/template'

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
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

#Function to clean up prompts1b
def cleanup(versionnegopath):
    for filename in os.listdir(versionnegopath):
        filename = versionnegopath + "/" + filename
        print(filename)
        with open(filename, 'r') as file:
            lines = file.readlines()

        result = []
        inside_supported_version = False
        combined_line = ""

        for line in lines:
            if '{' in line and '}' in line:
                # Extract content between the curly braces
                inner_content = line.split('{')[1].split('}')[0]
                
                # Split the inner content by commas
                items = inner_content.split(',')

                for item in items:
                    # print('aaa', item)
                    result.append(item)
            
            else:
                stripped_line = line.strip()
                # print('stripped line: ', stripped_line)

                if '`' in stripped_line or '{' in stripped_line or '}' in stripped_line: continue

                if '//' in stripped_line:
                    stripped_line = line.split('//')[0].strip()

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

# cleanup('input/prompts1b/versionnego/all')
# cleanup('input/prompts1b/versionnego/template')
# cleanup('input/prompts1b/initial/template')
# cleanup('input/prompts1b/initial/all')
# cleanup('input/prompts1b/0rtt/all')
# cleanup('input/prompts1b/0rtt/template')
# cleanup('input/prompts1b/handshake/all')
# cleanup('input/prompts1b/handshake/template')
# cleanup('input/prompts1b/retry/all')
# cleanup('input/prompts1b/retry/template')
cleanup('input/prompts1b/1rtt/all')
cleanup('input/prompts1b/1rtt/template')