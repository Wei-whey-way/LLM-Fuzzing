#File to create batch prompt format for prompts 1b. Run this code after running task1b_extractor
import os
from pathlib import Path
import json

# bytestream_dir = 'input/prompts1b'
output_dir = 'input/batchinputprompts'

#Make output folder
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if os.path.exists('input/batchinputprompts/2-batchprompts'): os.remove('input/batchinputprompts/2-batchprompts')
if os.path.exists('input/batchinputprompts/batchprompts.jsonl'): os.remove('input/batchinputprompts/batchprompts.jsonl')


def bytestream_extract_2(path):
    prompt_list = []

    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file == 'seperated_encrypted.txt':
                # Construct the full file path
                file_path = os.path.join(subdir, file)
                prompt = "The RFC9000 QUIC protocol, as stated in this document https://www.rfc-editor.org/rfc/rfc9000.html, contains packet formats for long and short header packets. The long packets are: Version Negotiation Packet, Initial Packet, 0-RTT Packet, Handshake Packet, and Retry Packet. The short header packets are: 1-RTT Packet.\n\nI have these hex bytestreams. Identify what packet they belong to and if there are missing packets, name what they are and create a valid hex string for that packet. "
     
                # Open and read the contents of the file
                with open(file_path, 'r') as f:
                    for i, line in enumerate(f):
                        line = f"Line {i+1}: {line}"
                        prompt += line

                    prompt += "\nProvide output in the following format:\n{Line x, x is the number of line given in prompt. Do not give bytestream}: {Packet header of the line}\n\nMissing packets:\n{name of missing packet }: {bytestream for missing packet}. {Line y, y is x+1. Do not give bytestream}: {Packet header of the line}\n\nPlace the missing packet in the correct position between the lines provided. Give only the output, no conversation."
                    # print('AAAA', len(prompt)/3)

                    #Skip prompts that are too long
                    if (len(prompt)/3 > 4096): continue

                    prompt_list.append(prompt)
                    
                    #End condition
                    if(len(prompt_list)) >= 50: 
                        # print(prompt_list)
                        return prompt_list #End function if length is 50
                
    return prompt_list
                    
#Create prompts
def generate_batch_prompts(task2_prompts):
    for i, prompt in enumerate(task2_prompts):
        # print(task1)
        # print(task2)
        
        #Calculating max_tokens NOTE can only go up to 4096
        max_tokens = int(len(prompt)/3)

        #Creating batch prompt
        gpt_prompt = {"custom_id": f"request-{i+1}", 
                      "method": "POST", 
                      "url": "/v1/chat/completions", 
                      "body": {
                          "model": "gpt-4o", 
                          "messages": [
                            {"role": "system", "content":  prompt,},
                        ],
                      "max_tokens": max_tokens}}
        
        with open('input\\batchinputprompts\\2-batchprompts.jsonl', 'a') as file:
            file.write(json.dumps(gpt_prompt) + '\n')
            
#Get bytestream for second part
task2_input_path = Path('input//task_2_training_data')
task2_prompts = bytestream_extract_2(task2_input_path)

#Generate gpt prompts
generate_batch_prompts(task2_prompts)