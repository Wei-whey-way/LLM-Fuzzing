#Evaluations for prompt 3
import os
import re
import glob
from collections import Counter

# path_1rtt = 'output\\prompts3\\1rtt\\all'
path_1rtt = 'output\\prompts3\\1rtt\\baseline'
# path_1rtt = 'output\\prompts3\\1rtt\\persona'
# path_1rtt = 'output\\prompts3\\1rtt\\rag'
# path_retry = 'output\\prompts3\\retry\\all'
path_retry = 'output\\prompts3\\retry\\baseline'
# path_retry = 'output\\prompts3\\retry\\persona'
# path_retry = 'output\\prompts3\\retry\\context'
# path_retry = 'output\\prompts3\\retry\\rag'
destination_dir = 'output\\prompts3\\eval'
prompt3_output_files = []

# Create the evaluation directory if it doesn't exist
if not os.path.exists(destination_dir): os.makedirs(destination_dir)

#Get a sorted list of files that match the pattern output1-50.txt
file_list_1rtt = glob.glob(os.path.join(path_1rtt, 'output*.txt'))
file_list_1rtt.sort(key=lambda f: int(os.path.basename(f).split('output')[1].split('.')[0]))
file_list_retry = glob.glob(os.path.join(path_retry, 'output*.txt'))
file_list_retry.sort(key=lambda f: int(os.path.basename(f).split('output')[1].split('.')[0]))

#Create list of ground truth packets
def generate_gt(gt_path):
    gt_list = []
    with open(gt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            bytestream = line.split(':')[1].strip()
            # print(bytestream)

            #Find out what packet is from bytestream
            binary = bytestream[:1]        
            binary = bin(int(binary, 16))[2:].zfill(4)
            if (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '00'): 
                gt_list.append('Initial')           #Initial
                # des_connect_id = bytestream[12:28]
                # print('Des connection id:', des_connect_id)
            elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '01'): 
                gt_list.append('0-RTT')           #0-rtt
            elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '10'): 
                gt_list.append('Handshake')       #Handshake
            elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '11'): 
                gt_list.append('Retry')           #Retry
            elif (binary[0]=='0'):
                if (bytestream[2:10] == '00000000'): 
                    gt_list.append('Version Negotiation')                      #Version nego
                elif (binary[1] == '1'): 
                    gt_list.append('1-rtt')                                    #1-rtt
                    # des_connect_id = bytestream[2:18]
                    # print('Des connection id (1rtt):', des_connect_id)
                else: 
                    print('Uh oh with start 0', binary)
                    continue
            else:
                print('Check this:', line, '\n\t in binary', binary)
                continue
    return gt_list

gt_list_1rtt = generate_gt('input\\prompts3\\groundtruth\\1rtt.txt')
gt_list_retry = generate_gt('input\\prompts3\\groundtruth\\retry.txt')

# print('ground truth:', gt_list_1rtt)
def eval(packets, file_list, gt_list):
    state_success_count = {'1-RTT': 0, 'Retry': 0}
    state_fail_count = {'1-RTT': 0, 'Retry': 0}
    partial_list = {'1-RTT': 0, 'Retry': 0}
    hallu_list = {'1-RTT': 0, 'Retry': 0}
    
    # print(file_list)
    for i, file in enumerate(file_list): #Read through each output
        #Ground truth file
        gt_file = gt_list[i]
        # print(file, '\tGround truth: ', gt_file)

        with open(file, 'r', encoding='utf-8') as f:
            lines = [line.replace('*','').replace('`','').strip() for line in f.readlines() if '`' not in line and line.strip()]
            # print(lines)

            #Check if format is followed (Packet name: Bytestream. If separated, combine with next line)
            # print(lines[0].split(': '))
            # split_lines = lines[0].split(':')
            try:
                split_lines = [item.strip() for item in lines[0].split(':') if item.strip()]
            except IndexError: #Outputs that aren't formatted properly
                hallu_list[packets] += 1
                continue
            
            # print(split_lines)

            #Extracting bytestream
            if len(split_lines) > 1:
                # print(split_lines)
                packet = split_lines[0].strip()
                bytestream = split_lines[1].strip()
                # print(packet, bytestream)
            else:
                if any(char.isdigit() for char in split_lines[0]): #Check if line only contains digits (bytestream)
                    # print(split_lines, "contains numbers.")
                    bytestream = split_lines[0]
                else: #Get bytestream from next line
                    # print("The string does not contain numbers. Looking at next line...\n", lines[1]) 
                    bytestream = lines[1]
            
            #Preprocessing bytestream
            if('0x') in bytestream[:2]: bytestream = bytestream[2:]
            bytestream = bytestream.replace(' ','')
            # print(bytestream)

            #Check if bytestream is a valid hexadecimal string
            is_hex = all(char in '0123456789abcdefABCDEF' for char in bytestream)
            if not (is_hex): #Skip invalid bytestream
                hallu_list[packets] += 1
                continue
            
            #Check header form
            cut_bytestream = bytestream[:1]
            binary = bin(int(cut_bytestream, 16))[2:].zfill(4)
            # print(binary)

            if binary[0] == '1': #Long header packets + Version nego
                # print('Checking for long header packets', bytestream)
                
                #Check version
                version = bytestream[2:10]
                # print('Version', version)

                if version == '00000000': #Check for version nego
                    # print('Version = 0: ', bytestream, '\n')
                    
                    #Check header form (1) = 1
                    cut_bytestream = bytestream[:1]
                    binary = bin(int(cut_bytestream, 16))[2:].zfill(4)

                    #Check for destination connection id:
                    des_connect_id = bytestream[12:28]

                    
                    if binary[0] == '1':
                        if des_connect_id == '1d5b0380bd0c3907': #This is an old version of above
                            if(gt_file) == 'Version nego': 
                                state_success_count[packets] += 1
                                print('AAAAA')
                            else: state_fail_count[packets] += 1
                        else:
                            partial_list[packets] += 1
                            state_fail_count[packets] += 1
                    else:
                        # print('Hallucination (version nego)', bytestream)
                        hallu_list[packets] += 1
                        
                elif version == '00000001': #Check for long header packets
                    # print('Version = 1: ', bytestream)

                    #Check destination connection id
                    des_connect_id = bytestream[12:28]

                    #Check packet type
                    cut_bytestream = bytestream[:1]
                    binary = bin(int(cut_bytestream, 16))[2:].zfill(4)

                    if binary == '1100': packet_type = 'Initial'
                    elif binary == '1101': packet_type = '0-RTT'
                    elif binary == '1110': packet_type = 'Handshake'
                    elif binary == '1111': packet_type = 'Retry'
                    else:
                        # print('Error in reading binary for version 1', bytestream, packets)
                        hallu_list[packets] += 1 
                        continue  
                    
                    #Check for successful state transiton
                    # print(f'{packets} (GT): {packet_type} comparing with', gt_file, packet_type == gt_file)
                    match packets:
                        case '1-RTT':
                            if(packet_type == 'Initial' or packet_type == '1-rtt'):
                                if (des_connect_id == '1d5b0380bd0c3907'):
                                    state_success_count[packets] += 1
                                    print('It worked!', bytestream)
                                else:
                                    partial_list[packets] += 1
                                    state_fail_count[packets] += 1
                            else:
                                state_fail_count[packets] += 1
                        case 'Retry':
                            if(packet_type == 'Initial' or packet_type == 'Retry'):
                                if (des_connect_id == '1d5b0380bd0c3907'):
                                    state_success_count[packets] += 1
                                else:
                                    partial_list[packets] += 1
                                    state_fail_count[packets] += 1
                            else:
                                state_fail_count[packets] += 1
                    
                    
                else:
                    # print('Hallucination (long header)')
                    hallu_list[packets] += 1            
            
            else: #Bytestream generated is 1-rtt
                # print('Check for 1-rtt', binary)

                #Check dest connection id
                des_connect_id = bytestream[2:18]
                # print('Des connection id (LLM-1rtt):', des_connect_id)

                #Check for spin bit
                if binary[1] == '1': 
                    # print('LLM generates 1-RTT. Checking ground truth:', gt_file)
                    if(gt_file) == '1-rtt' and des_connect_id=='1d5b0380bd0c3907':
                        # print('Success!')
                        state_success_count[packets] += 1
                    else:
                        state_fail_count[packets] += 1
                else:
                    # print('Hallucination (1-rtt)\n')
                    hallu_list[packets] += 1
    
    print(f'{packets} metrics:')
    print('\tState transition success:', state_success_count[packets])
    print('\tState transition fail:', state_fail_count[packets])
    print('\tHallucinations:', hallu_list[packets])
    print('\tPartial state:', partial_list[packets])

    return

#Split file_list_1rtt into state 1 (odd) and state 2 (event). Same for ground truth
file_list_1rtt_state1 = [file_list_1rtt[i] for i in range(len(file_list_1rtt)) if i % 2 == 0]  # even indices
gt_list_1rtt_state1 = [gt_list_1rtt[i] for i in range(len(gt_list_1rtt)) if i % 2 == 0]

file_list_1rtt_state2 = [file_list_1rtt[i] for i in range(len(file_list_1rtt)) if i % 2 != 0]  # odd indices
gt_list_1rtt_state2 = [gt_list_1rtt[i] for i in range(len(gt_list_1rtt)) if i % 2 != 0]
# print(file_list_1rtt_state1)

eval('1-RTT', file_list_1rtt_state1, gt_list_1rtt_state1)
# eval('1-RTT', file_list_1rtt_state2, gt_list_1rtt_state2)
# eval('Retry', file_list_retry, gt_list_retry)