#File to read in prompts from batchinputs and extracts content from ChatGPT batch files
import os
import json
import re

path = 'input\\batchinputs'
files = []

#Put all inputs into files vector
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    folder_name = None

    #Reading in output file
    with open(filepath, "r") as file:
        inputs = file.readlines()
    
        if re.match(r'raw_prompts2_[1-9]\.jsonl', filename):
            if not os.path.exists('output/prompts2/all'): os.makedirs('output/prompts2/all')
            folder_name = 'output/prompts2/all'
        
        elif re.match(r'raw_prompts2_template\.jsonl', filename):
            if not os.path.exists('output/prompts2/template'): os.makedirs('output/prompts2/template')
            folder_name = 'output/prompts2/template'
        
        elif re.match(r'raw_prompts2_context\.jsonl', filename):
            if not os.path.exists('output/prompts2/context'): os.makedirs('output/prompts2/context')
            folder_name = 'output/prompts2/context'
        
        elif re.match(r'raw_prompts2_baseline\.jsonl', filename):
            if not os.path.exists('output/prompts2/baseline'): os.makedirs('output/prompts2/baseline')
            folder_name = 'output/prompts2/baseline'
        
        elif re.match(r'raw_prompts2_rag\.jsonl', filename):
            if not os.path.exists('output/prompts2/rag'): os.makedirs('output/prompts2/rag')
            folder_name = 'output/prompts2/rag'
        
        elif re.match(r'raw_prompts3_1rtt\.jsonl', filename):
            if not os.path.exists('output/prompts3/1rtt/all'): os.makedirs('output/prompts3/1rtt/all')
            folder_name = 'output/prompts3/1rtt/all'

        elif re.match(r'raw_prompts3_1rtt_baseline\.jsonl', filename):
            if not os.path.exists('output/prompts3/1rtt/baseline'): os.makedirs('output/prompts3/1rtt/baseline')
            folder_name = 'output/prompts3/1rtt/baseline'
        
        elif re.match(r'raw_prompts3_1rtt_persona\.jsonl', filename):
            if not os.path.exists('output/prompts3/1rtt/persona'): os.makedirs('output/prompts3/1rtt/persona')
            folder_name = 'output/prompts3/1rtt/persona'
        
        elif re.match(r'raw_prompts3_1rtt_context\.jsonl', filename):
            if not os.path.exists('output/prompts3/1rtt/context'): os.makedirs('output/prompts3/1rtt/context')
            folder_name = 'output/prompts3/1rtt/context'
        
        elif re.match(r'raw_prompts3_1rtt_rag\.jsonl', filename):
            if not os.path.exists('output/prompts3/1rtt/rag'): os.makedirs('output/prompts3/1rtt/rag')
            folder_name = 'output/prompts3/1rtt/rag'

        elif re.match(r'raw_prompts3_retry\.jsonl', filename):
            if not os.path.exists('output/prompts3/retry/all'): os.makedirs('output/prompts3/retry/all')
            folder_name = 'output/prompts3/retry/all'

        elif re.match(r'raw_prompts3_retry_baseline\.jsonl', filename):
            if not os.path.exists('output/prompts3/retry/baseline'): os.makedirs('output/prompts3/retry/baseline')
            folder_name = 'output/prompts3/retry/baseline'
        
        elif re.match(r'raw_prompts3_retry_persona\.jsonl', filename):
            if not os.path.exists('output/prompts3/retry/persona'): os.makedirs('output/prompts3/retry/persona')
            folder_name = 'output/prompts3/retry/persona'
        
        elif re.match(r'raw_prompts3_retry_context\.jsonl', filename):
            if not os.path.exists('output/prompts3/retry/context'): os.makedirs('output/prompts3/retry/context')
            folder_name = 'output/prompts3/retry/context'
        
        elif re.match(r'raw_prompts3_retry_rag\.jsonl', filename):
            if not os.path.exists('output/prompts3/retry/rag'): os.makedirs('output/prompts3/retry/rag')
            folder_name = 'output/prompts3/retry/rag'
        
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
            # print(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)