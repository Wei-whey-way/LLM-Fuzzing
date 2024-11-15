#File to create batch prompt format for prompts 3 and ground truth. Run this code after running task1b_extractor
import os
from pathlib import Path
import json

# prompt_dir = 'input/prompts1b'
output_dir = 'input/prompts3'
prompt_dir = 'input/prompts3/prompts'
prompt_1rtt = 'input/prompts3/prompts/1rtt'
prompt_retry = 'input/prompts3/prompts/retry'
gt_path = 'input/prompts3/groundtruth'

#Make output folder
if not os.path.exists(prompt_dir): os.makedirs(prompt_dir)
if not os.path.exists(prompt_1rtt): os.makedirs(prompt_1rtt)
if not os.path.exists(prompt_retry): os.makedirs(prompt_retry)
if not os.path.exists(gt_path): os.makedirs(gt_path)

# if os.path.exists('input/prompts3'): os.remove('input/batchinputprompts/')
# if os.path.exists('input/batchinputprompts/batchprompts.jsonl'): os.remove('input/batchinputprompts/batchprompts.jsonl')

def generate_prompt(string):
    prompt = "The RFC9000 QUIC protocol, as stated in this document https://www.rfc-editor.org/rfc/rfc9000.html, contains packet formats for long and short packets.\nYour role is the client of a QUIC protocol that is communicating with the server. In the QUIC protocol, you have received the following communication history between the QUIC client and the QUIC server. From the communication history between client and server, create what you think the next packet type should be as well as creating a bytestream that follows the rules of that packet type.\nCommunication history:\n```\n"
    prompt += string
    prompt += "```\nThis is the desired format:\n{Packet type of next client request}: {Bytestream that follows the rules of that packet type}\nDo not give explanation on the communication history. I only want the output of the created packet type and its bytestream. No conversation, give only the output."
    
    # print(prompt, '\n')
    return prompt

def prompt_cut_1rtt(path):
    gt_path_1rtt = 'input/prompts3/groundtruth/1rtt.txt'
    prompt_list = []
    hex_list = []
    hex_files = []
    file_count = 0 #For debugging

    print(f'{gt_path_1rtt}')
    f = open(gt_path_1rtt, "w")
    f.close()

    for subdir, dirs, files in os.walk(path):
        # print(subdir)
        # print(hex_list, len(hex_list))
        if(file_count >= 100): return
        
        for file in files:
            if file == 'seperated_encrypted.txt':
                # Construct the full file path
                file_path = os.path.join(subdir, file)
                # print(file_path)
                
                # Open and read the contents of the file
                with open(file_path, 'r') as f:
                    lines = [line.strip().replace(" ","") for line in f.readlines()]
                    # print(lines)

                    #Generating prompts
                    list_1 = lines[:6]
                    list_2 = lines[:13]
                    # print(list_1[len(list_1)-1])
                    # print(list_2[len(list_2)-1])
                    string_1 = ""
                    string_2 = ""

                    print(f'AAA {prompt_dir}/1rtt/{file_count}_{subdir.replace("input\\task_3_training_data\\", "")}.txt')
                    file_count+=1
                    f = open(f'{prompt_dir}/1rtt/{file_count}_{subdir.replace("input\\task_3_training_data\\", "")}.txt', "w")
                    for line in list_1: string_1 += line + "\n"
                    prompt = generate_prompt(string_1)
                    f.write(prompt)
                    f.close()
                    
                    file_count+=1
                    f = open(f'{prompt_dir}/1rtt/{file_count}_{subdir.replace("input\\task_3_training_data\\", "")}.txt', "w")
                    for line in list_2: string_2 += line + "\n"
                    prompt = generate_prompt(string_2)
                    f.write(prompt)
                    f.close()

                    #Ground truth values
                    # print(f'Ground truth list_1: {lines[6]}\t\t{subdir}\nGround truth list_2: {lines[13]}\t\t{subdir}')
                    with open(gt_path_1rtt, 'a') as f:
                        f.write(f'{subdir} | List_1: {lines[6]}\n')
                        f.write(f'{subdir} | List_2: {lines[13]}\n')
    return

def prompt_cut_retry(path):
    gt_path_retry = 'input/prompts3/groundtruth/retry.txt'
    
    prompt_list = []
    hex_list = []
    hex_files = []
    file_count = 0 #For debugging

    print(f'{gt_path_retry}')
    f = open(gt_path_retry, "w")
    f.close()

    for subdir, dirs, files in os.walk(path):
        # print(subdir)
        # print(hex_list, len(hex_list))
        if(file_count >= 100): return
        
        for file in files:
            if file == 'seperated_encrypted.txt':
                # Construct the full file path
                file_path = os.path.join(subdir, file)
                # print(file_path)
                
                # Open and read the contents of the file
                with open(file_path, 'r') as f:
                    lines = [line.strip().replace(" ","") for line in f.readlines()]
                    # print(lines)

                    #Generating prompts
                    list_1 = lines[:2]
                    # print(list_1[len(list_1)-1])
                    string_1 = ""

                    # print(f'AAA {prompt_dir}/retry/{file_count}_{subdir.replace("input\\task_3_training_data_retry\\", "")}.txt')
                    file_count+=1
                    f = open(f'{prompt_dir}/retry/{file_count}_{subdir.replace("input\\task_3_training_data_retry\\", "")}.txt', "w")
                    for line in list_1: string_1 += line + "\n"
                    prompt = generate_prompt(string_1)
                    f.write(prompt)
                    f.close()
                    
                    #Ground truth values
                    # print(f'Ground truth list_1: {lines[6]}\t\t{subdir}\nGround truth list_2: {lines[13]}\t\t{subdir}')
                    with open(gt_path_retry, 'a') as f:
                        f.write(f'{subdir} | List_1: {lines[2]}\n')
    return

def generate_batch_prompts(model, packet_type=None):
    match packet_type:
        case '1-rtt': 
            folder_path = 'input/prompts3/prompts/1rtt'
            output_path = 'input\\batchinputprompts\\3-batchprompts-1rtt.jsonl'
        case 'retry': 
            folder_path = 'input/prompts3/prompts/retry'
            output_path = 'input\\batchinputprompts\\3-batchprompts-retry.jsonl'
        case _:
            print('Error in packet types (generate batch prompts)')
            return

    f = open(output_path, "w") #Create new file
    f.close()

    # Extract numeric parts and sort by them
    files = os.listdir(folder_path)
    # print('AAA', files)
    files = sorted(files, key=lambda x: int(x.split('_')[0]))
    # print('AAAA', files)

    for i, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # print(i+1, file_path)

            with open(file_path, 'r') as f:
                prompt = f.read()
                # print(prompt)
            
            token_length = min(int(len(prompt) / 4 + 1000), 4096)
            # print(token_length)

            gpt_prompt = {"custom_id": "request-"+str(i+1), 
                            "method": "POST", 
                            "url": "/v1/chat/completions", 
                            "body": {"model": model, 
                                    "messages": [
                                        {"role": "system", 
                                        "content": prompt
                                        }],
                                        "max_tokens": token_length}}

            with open(output_path, 'a') as file:
                file.write(json.dumps(gpt_prompt) + '\n')

    return

#Get bytestream for second part
task3_input_path_1rtt = Path('input//task_3_training_data')
task3_bytestreams_1rtt = prompt_cut_1rtt(task3_input_path_1rtt)

task3_input_path_retry = Path('input//task_3_training_data_retry')
# task3_bytestreams_retry = prompt_cut_retry(task3_input_path_retry)

#Generate gpt prompts
generate_batch_prompts("gpt-4o", '1-rtt')
# generate_batch_prompts("gpt-4o", 'retry')