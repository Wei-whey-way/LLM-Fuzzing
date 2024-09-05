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
if os.path.exists('input/batchinputprompts/test.jsonl'): os.remove('input/batchinputprompts/test.jsonl')


#Function to extract 'messages' from each line in batchinput prompts (Get chatgpt output)
def gpt_extract(file_location):
    hex_list = []
    print(file_location)

    # Open the file and process it line by line
    with open(file_location, 'r') as file:
        gpt_output_1a_list = []
        
        for i, data in enumerate(file):
            data = json.loads(data)
            
            message_content = data['response']['body']['choices'][0]['message']['content']
            # Remove 'refusal' key if it exists
            if 'refusal' in message_content:
                del message_content['refusal']
            
            # if(i==0): print(message_content)
            
            gpt_output_1a_list.append(message_content)

            # new_prompt = generate_batch_prompt()
    
    return gpt_output_1a_list

def bytestream_extract_2(path):
    prompt_list = []
    debug_first = True #For debugging

    for subdir, dirs, files in os.walk(path):
        # print(len(bytestream_list))
        
        # print(f'subdir:{subdir}\tdirs:{dirs}')
        for file in files:
            part_2_dict = {}
            if file == 'seperated_encrypted.txt':
                # Construct the full file path
                file_path = os.path.join(subdir, file)
                prompt = "I now have a bytestream containing multiple strings in hexadecimal. Identify the name of the packet for each line of the bytestream\n\nBytestream: \n"
                        
                # Open and read the contents of the file
                with open(file_path, 'r') as f:
                    for i, line in enumerate(f):
                        line = f"Line {i}: {line}"
                        prompt += line

                    prompt += "\nProvide output in the following format:\n{Line x, x is the number of line given in prompt. Do not give bytestream}: {Packet header of the line}\n\nMissing packets:\n{name of missing packet }: {bytestream for missing packet}. {Line y, y is x+1. Do not give bytestream}: {Packet header of the line}\n\nPlace the missing packet in the correct position between the lines provided."
                    # print(prompt)

                    # part_2_dict.update({'role':'user', 'content': prompt})
                    # print(part_2_dict)
                    prompt_list.append(prompt)

                    # print('Length prompt list: ', len(prompt_list))
                    # if(debug_first == True):
                    #     print('appended: ', prompt_list)
                    #     debug_first = False
                    
                    #End condition
                    if(len(prompt_list)) >= 50: 
                        # print(prompt_list)
                        return prompt_list #End function if length is 50
                
    return prompt_list
                    
#Create prompts
def merge_prompts(task1_prompts, task2_prompts):
    # merged_prompts = 
    #Original prompts for 1a
    task1a_prompt = "For the RFC9000 QUIC protocol, please provide all of the packet grammar specified in the document. You can find the document here - https://www.rfc-editor.org/rfc/rfc9000.html\n\nDesired Format:\nShot-1:\nFor the QUIC protocol, the Retry Packet client request format is below. See RFC9000 for set bytes.\\nRetry Packet: {Header Form (1): <Value>\\\\r\\\\n, Fixed Bit (1): <Value>\\\\r\\\\n, Long Packet Type (2): <Value>\\\\r\\\\n, Unused (4): <Value>\\\\r\\\\n, Version (32): <Value>\\\\r\\\\n, Destination Connection ID Length (8): <Value>\\\\r\\\\n, Destination Connection ID (0..160): <Value>\\\\r\\\\n, Source Connection ID Length (8): <Value>\\\\r\\\\n, Source Connection ID (0..160): <Value>\\\\r\\\\n, Retry Token (..): <Value>\\\\r\\\\n, Retry Integrity Tag (128) <Value>\\\\r\\\\n}\n\nShot-2:\n0-RTT Packet: {Header Form (1): <Value>\\\\r\\\\n, Fixed Bit (1): <Value>\\\\r\\\\n, Long Packet Type (2): <Value>\\\\r\\\\n, Reserved Bits (2): <Value>\\\\r\\\\n, Packet Number Length (2): <Value>\\\\r\\\\n, Version (32): <Value>\\\\r\\\\n, Destination Connection ID Length (8): <Value>\\\\r\\\\n, Destination Connection ID (0..160): <Value>\\\\r\\\\n, Source Connection ID Length (8): <Value>\\\\r\\\\n, Source Connection ID (0..160): <Value>\\\\r\\\\n, Length (i): <Value>\\\\r\\\\n, Packet Number (8..32): <Value>\\\\r\\\\n, Packet Payload (8..): <Value>\\\\r\\\\n,}\n\nPlease provide all of the Long Header Packets and all of the Short Header Packets in the desired format according to RFC9000 documentation. Make sure to name all the header packets correctly. Display the packets line by line. For header form, fixed bit, long packet type, fill in the <Value> field to a value that is suitable based on the document that I linked above. <Value> format in hexadecimal. If the <Value> depends on the information during transmission, just remain <Value>.\n\nProvide output in this format:\\n[Packet name]: {Packet content 1, content 2}\nGive me only the requested output, no conversation."
    
    prompt_parameters = zip(task1_prompts, task2_prompts)
    for i, (task1, task2) in enumerate(prompt_parameters):
        # print(task1)
        # print(task2)
        
        #Calculating max_tokens NOTE can only go up to 4096
        max_tokens = (len(task1a_prompt) + len(task1) + len(task2))/3
        max_tokens = 4096

        #Creating batch prompt
        gpt_prompt = {"custom_id": f"request-{i+1}", 
                      "method": "POST", 
                      "url": "/v1/chat/completions", 
                      "body": {
                          "model": "gpt-4o", 
                          "messages": [
                            {"role": "system", "content":  task1a_prompt,},
                            {"role": "assistant", "content": task1},
                            {"role": "user", "content": task2}
                        ],
                      "max_tokens": max_tokens}}
        
        with open('input\\batchinputprompts\\test.jsonl', 'a') as file:
            file.write(json.dumps(gpt_prompt) + '\n')
            

#Put all inputs into files list
task1a_batch_output = Path('input//batchinputs//raw_prompts1a.jsonl')
task1a_prompts = gpt_extract(task1a_batch_output)

#Get bytestream for second part
task2_input_path = Path('input//task_2_training_data')
task2_prompts = bytestream_extract_2(task2_input_path)
# for item in task2_bytestream_list: print(item)

#Merge task1a and task2 prompts together
merge_prompts(task1a_prompts, task2_prompts)