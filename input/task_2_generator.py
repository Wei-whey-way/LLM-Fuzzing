#File to create batch prompt format for prompts 1b. Run this code after running task1b_extractor
import os
from pathlib import Path
import json

# bytestream_dir = 'input/prompts1b'
output_dir = 'input/batchinputprompts'
gt_output_dir = 'input/prompts2/groundtruth'

#Make output folder
if not os.path.exists(output_dir): os.makedirs(output_dir)
if not os.path.exists(gt_output_dir): os.makedirs(gt_output_dir)

if os.path.exists('input/batchinputprompts/2-batchprompts'): os.remove('input/batchinputprompts/2-batchprompts')
if os.path.exists('input/batchinputprompts/batchprompts.jsonl'): os.remove('input/batchinputprompts/batchprompts.jsonl')

def ground_truth_generator(prompts, file_names):
    files = zip(prompts, file_names)
    two_packets_count = 0 
    three_packets_count = 0
    
    for i, (prompt, prompt_path) in enumerate(files):
        # #Prompts is the list of hexstream. Each hexstream is a list containing each line of the hexstream (list of lists) 
        file_name = gt_output_dir + f'/{i+1}.txt'
        # print('File name: ', file_name)

        #Create file and remove previous content
        with open(file_name, 'w') as f:
            f.write(prompt_path + '\n') #State where file is from

        #Initialize a dictionary to count packet types
        packet_counts = {'Initial Packet': 0, '0-RTT Packet': 0, 'Handshake Packet': 0, 'Retry Packet': 0, '1-RTT Packet':0}

        for line in prompt:
            with open(file_name, 'a') as f:
                line = line.strip().replace(' ','') #Preprocessing
                
                binary = line[:1] #Get first characters in hex
                binary = bin(int(binary, 16))[2:].zfill(4) #zfill to make sure that leading 0s are kept
                # print('Binary: ', binary)

                #Get packet name
                if (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '00'): 
                    f.write('Initial | ') #Initial packet
                    packet_counts['Initial Packet'] += 1
                elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '01'): 
                    f.write('0rtt | ') #0-Rtt
                    packet_counts['0-RTT Packet'] += 1
                elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '10'): 
                    f.write('Handshake | ') #Handshake
                    packet_counts['Handshake Packet'] += 1
                elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '11'): 
                    f.write('Retry | ') #Retry
                    packet_counts['Retry Packet'] += 1
                elif (binary[0]=='0' and binary[1]=='1'):
                    f.write('1rtt | ') #1-Rtt
                    packet_counts['1-RTT Packet'] += 1
                
                f.write(line + '\n')
        
        # Calculate the number of distinct packet types
        distinct_packet_types = sum(1 for count in packet_counts.values() if count > 0)

        match distinct_packet_types:
            case 2:
                if two_packets_count > 50: continue
                two_packets_count +=1
            case 3:
                if three_packets_count > 50: continue
                three_packets_count +=1

        # Write the number of distinct packet types at the end of the file
        with open(file_name, 'a') as f:
            f.write(f'\nNumber of unique packet types: {distinct_packet_types}\n')
            f.write(f'{packet_counts}\n')
        
    print('Final packet count tally:\n\t(2)', two_packets_count, '\n\t(3)', three_packets_count)
    return

def count_unique_packets(hex_list):
    # print(hex_list)

    #Initialize a dictionary to count packet types
    packet_counts = {'Initial Packet': 0, '0-RTT Packet': 0, 'Handshake Packet': 0, 'Retry Packet': 0, '1-RTT Packet':0}

    for line in hex_list:
        binary = line[:1] #Get first characters in hex
        binary = bin(int(binary, 16))[2:].zfill(4) #zfill to make sure that leading 0s are kept
        # print('Binary: ', binary
        #Get packet name
        if (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '00'):
            packet_counts['Initial Packet'] += 1
        elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '01'): 
            packet_counts['0-RTT Packet'] += 1
        elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '10'):
            packet_counts['Handshake Packet'] += 1
        elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '11'):
            packet_counts['Retry Packet'] += 1
        elif (binary[0]=='0' and binary[1]=='1'): 
            packet_counts['1-RTT Packet'] += 1
        
    # Calculate the number of distinct packet types
    distinct_packet_types = sum(1 for count in packet_counts.values() if count > 0)
    return distinct_packet_types

def bytestream_extract_2(path):
    prompt_list = []
    hex_list = []
    hex_files = []
    two_packets_count = 0
    three_packets_count = 0

    for subdir, dirs, files in os.walk(path):
        # print(subdir)
        for file in files:
            if file == 'seperated_encrypted.txt':
                # Construct the full file path
                file_path = os.path.join(subdir, file)
                prompt = "The RFC9000 QUIC protocol, as stated in this document https://www.rfc-editor.org/rfc/rfc9000.html, contains packet formats for long and short header packets. The long packets are: Version Negotiation Packet, Initial Packet, 0-RTT Packet, Handshake Packet, and Retry Packet. The short header packets are: 1-RTT Packet.\n\nI have these hex bytestreams. Identify what packet they belong to and if there are missing packets, name what they are and create a valid hex string for that packet. If multiple packet types are missing, provide only one packet for each packet type."
                gt_hex = []
                # Open and read the contents of the file
                with open(file_path, 'r') as f:
                    for i, line in enumerate(f):
                        line = line.replace(' ','')
                        gt_hex.append(line)
                        line = f"Line {i+1}: {line}"
                        prompt += line

                    prompt += "\nProvide output in the following format:\n{Line x, x is the number of line given in prompt. Do not give bytestream}: {Packet header of the line}\n\nMissing packets:\n{name of missing packet }: {bytestream for missing packet}. {Line y, y is x+1. Do not give bytestream}: {Packet header of the line}\n\nPlace the missing packet in the correct position between the lines provided. Give only the output, no conversation."
                    # print('AAAA', gt_hex)

                    #Get unique packet type count for gt_hex
                    unique_packet_count = count_unique_packets(gt_hex)

                    match unique_packet_count:
                        case 2:
                            if two_packets_count > 50: continue
                            two_packets_count += 1
                            
                        case 3:
                            if three_packets_count > 50: continue
                            three_packets_count += 1
                            print('3 packets file: ', subdir)
                            
                        case _:
                            print('Unique packets: ', unique_packet_count, subdir)

                    #Skip prompts that are too long
                    if (len(prompt)/3 > 4444): continue
                    prompt_list.append(prompt)

                    #Append bytestream to create ground truth
                    # print(f'Using file {subdir}')
                    hex_list.append(gt_hex)
                    hex_files.append(subdir)

                    #End condition
                    if(two_packets_count >= 50 and three_packets_count >= 50): 
                        print('Prompt list: ', len(prompt_list), '2: ', two_packets_count, ', 3: ', three_packets_count)

                        #Generate ground truth for the hex strings
                        ground_truth_generator(hex_list, hex_files)
                        return prompt_list

    ground_truth_generator(hex_list, hex_files)            
    return prompt_list
                    
#Create prompts
def generate_batch_prompts(task2_prompts):
    f = open("input\\batchinputprompts\\2-batchprompts.jsonl", "w") #Create new file
    f.close()
    
    for i, prompt in enumerate(task2_prompts):
        # print(task2_prompts)
        
        #Calculating max_tokens NOTE can only go up to 4096
        max_tokens = min(int(len(prompt) / 4 + 1000), 4096)
        
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