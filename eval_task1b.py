#Evaluation for prompts1b
import os
import re
import matplotlib.pyplot as plt
from collections import Counter

path = 'input\\prompts1b'
files = []

#Initialise expected values for each packet type
expected_values = {
    "Version Negotiation Packet": {
        "Header Form (1)": "0x0",
        "Unused (7)": "<Value>",
        "Version (32)": "0x0",
        "Destination Connection ID Length (8)": "<Value>",
        "Destination Connection ID (0..2040)": "<Value>",
        "Source Connection ID Length (8)": "<Value>",
        "Source Connection ID (0..2040)": "<Value>",
        "Supported Version (32)": "<Value>",
    },
    "Initial Packet": {
        "Header Form (1)": "0x1",
        "Fixed Bit (1)": "0x1",
        "Long Packet Type (2)": "0x0",
        "Reserved Bits (2)": "<Value>",
        "Packet Number Length (2)": "<Value>",
        "Version (32)": "<Value>",
        "Destination Connection ID Length (8)": "<Value>",
        "Destination Connection ID (0..160)": "<Value>",
        "Source Connection ID Length (8)": "<Value>",
        "Source Connection ID (0..160)": "<Value>",
        "Token Length (i)": "<Value>",
        "Token (..)": "<Value>",
        "Length (i)": "<Value>",
        "Packet Number (8..32)": "<Value>",
        "Packet Payload (8..)": "<Value>",
    },
    "0-RTT Packet": {
        "Header Form (1)": "0x1",
        "Fixed Bit (1)": "0x1",
        "Long Packet Type (2)": "0x1",
        "Reserved Bits (2)": "<Value>",
        "Packet Number Length (2)": "<Value>",
        "Version (32)": "<Value>",
        "Destination Connection ID Length (8)": "<Value>",
        "Destination Connection ID (0..160)": "<Value>",
        "Source Connection ID Length (8)": "<Value>",
        "Source Connection ID (0..160)": "<Value>",
        "Length (i)": "<Value>",
        "Packet Number (8..32)": "<Value>",
        "Packet Payload (8..)": "<Value>",
    },
    "Handshake Packet": {
        "Header Form (1)": "0x1",
        "Fixed Bit (1)": "0x1",
        "Long Packet Type (2)": "0x2",
        "Reserved Bits (2)": "<Value>",
        "Packet Number Length (2)": "<Value>",
        "Version (32)": "<Value>",
        "Destination Connection ID Length (8)": "<Value>",
        "Destination Connection ID (0..160)": "<Value>",
        "Source Connection ID Length (8)": "<Value>",
        "Source Connection ID (0..160)": "<Value>",
        "Length (i)": "<Value>",
        "Packet Number (8..32)": "<Value>",
        "Packet Payload (8..)": "<Value>",
    },
    "Retry Packet": {
        "Header Form (1)": "0x1",
        "Fixed Bit (1)": "0x1",
        "Long Packet Type (2)": "0x3",
        "Unused (4)": "<Value>",
        "Version (32)": "<Value>",
        "Destination Connection ID Length (8)": "<Value>",
        "Destination Connection ID (0..160)": "<Value>",
        "Source Connection ID Length (8)": "<Value>",
        "Source Connection ID (0..160)": "<Value>",
        "Retry Token (..)": "<Value>",
        "Retry Integrity Tag (128)": "<Value>",
    },
    "1-RTT Packet": {
        "Header Form (1)": "0x0",
        "Fixed Bit (1)": "0x1",
        "Spin Bit (1)": "<Value>",
        "Reserved Bits (2)": "<Value>",
        "Key Phase (1)": "<Value>",
        "Packet Number Length (2)": "<Value>",
        "Destination Connection ID (0..160)": "<Value>",
        "Packet Number (8..32)": "<Value>",
        "Packet Payload (8..)": "<Value>",
    }
}

def extract_content(path):
    list_dict = []
    
    for i, filename in enumerate(os.listdir(path)):
        filepath = os.path.join(path,filename)
        # print(f'File {i+1}')
    
        # Reading in each file
        with open(filepath, "r") as file:
            dict = {}
            
            lines = file.readlines()

            for line in lines:
                #Remove leading and trailing whitespaces
                line = line.lstrip().strip()
                # print('Debugging Line first for loop: ', line)
           
                #Parse inputs that put all values in one line (Both curly bracers exist in the same line)
                if '{' in line and '}' in line:
                    # Remove the outer braces
                    line_content = line[line.find('{') + 1 : line.rfind('}')]

                    # Split the content by commas
                    pairs = line_content.split(',')

                    # print('pairs:\n\t', pairs)

                    for pair in pairs:
                        #Remove quotation marks from key value pairs
                        pair = pair.replace('"', '').replace(',', '')
                        # print('DEBUGGING: ', pair)

                        # Split each key-value pair by ':'
                        key_val_pair = pair.split(':')
                        key = key_val_pair[0].strip()  # Remove quotes and whitespace from key
                        val = key_val_pair[1].strip() if len(key_val_pair) > 1 else "None"  # Handle empty values

                        if val == None or val == "None": 
                            # print('\nval: ', val, '\n')
                            continue #Skip empty values
                        
                        # print('\t', key)
                        # if key == "Supported Version (32)":
                            # print('AAAA', val)
                        
                        dict[key] = val
                        # if('x' not in val.lower()):
                        # print(f'Appending: {val} to {key}')
                
                #Skip over lines that do not have quotation marks in them
                elif not '"' in line: continue 
                elif '{' in line or '}' in line: continue #Remove filler lines
                
                #Normal case
                else:
                    #Remove quotation marks from key value pairs
                    line = line.replace('"', '').replace(',', '')
                    # print('DEBUGGING line else condition:', line)
                    
                    # if (i==14): print('Now checking: ', line)
                    key_val_pair = line.split(':')
                    key = key_val_pair[0].strip()
                    val = key_val_pair[1].strip() if len(key_val_pair) > 1 and key_val_pair[1].strip() else None # Check if there is a value and set it to None if empty
                    # print(key_val_pair)
                    # print(key)
                    # print(val)

                    if(key == "Supported Version (32)"):
                        val = val.split()
                    
                    #Append key value pair to dictionary
                    dict[key] = val

        #Append dictionary into a list of dictionary
        list_dict.append(dict)

    # print('Extract content output:', list_dict)
    return list_dict

# Iterate through all subfolders in the root directory and extract contents into a list of dictionarys
versionnego_list = []
initial_list = []
zero_rtt_list = []
handshake_list = []
retry_list = []
one_rtt_list = []

for subdir, dirs, files in os.walk(path):
    # print(f'subdir:{subdir}\ndirs:{dirs}')
    # if subdir == 'input\\prompts1b\\initial\\all':
    #     initial_list = extract_content(subdir)

    # if subdir == 'input\\prompts1b\\initial\\template':
    #     initial_list = extract_content(subdir)
    
    # if subdir == 'input\\prompts1b\\initial\\rag': initial_list = extract_content(subdir)
        
    # if subdir == 'input\\prompts1b\\0rtt\\all':
    #     zero_rtt_list = extract_content(subdir)
    
    # if subdir == 'input\\prompts1b\\0rtt\\template':
    #     zero_rtt_list = extract_content(subdir)

    if subdir == 'input\\prompts1b\\0rtt\\rag': initial_list = extract_content(subdir)
    
    # if subdir == 'input\\prompts1b\\handshake\\all':
    #     handshake_list = extract_content(subdir)
    
    # if subdir == 'input\\prompts1b\\handshake\\template':
    #     handshake_list = extract_content(subdir)
    
    # if subdir == 'input\\prompts1b\\retry\\all': retry_list = extract_content(subdir)
    # if subdir == 'input\\prompts1b\\retry\\template': retry_list = extract_content(subdir)
    
    # if subdir == 'input\\prompts1b\\versionnego\\all':
    #     versionnego_list = extract_content(subdir)

    # if subdir == 'input\\prompts1b\\versionnego\\template': #NOTE For subdir, due to potato coding can only use one prompting method at one time
    #     versionnego_list = extract_content(subdir)

    # if subdir == 'input\\prompts1b\\1rtt\\all': one_rtt_list = extract_content(subdir)
    # if subdir == 'input\\prompts1b\\1rtt\\template': one_rtt_list = extract_content(subdir)

#Function to get number of packet fields extracted
def count_fields(dict_list, packet_type):
    num_fields_list = []
    missing_fields_list = []
    hallucinated_fields_list = []

    if packet_type == 'initial':
        expected_dict = expected_values["Initial Packet"]
        directory = 'input\\prompts1b\\groundtruth\\initial'
    elif packet_type == 'handshake':
        expected_dict = expected_values["Handshake Packet"]
        directory = 'input\\prompts1b\\groundtruth\\handshake'
    elif packet_type == 'retry':
        expected_dict = expected_values["Retry Packet"]
        directory = 'input\\prompts1b\\groundtruth\\retry'
    elif packet_type == '0rtt':
        expected_dict = expected_values["0-RTT Packet"]
        directory = 'input\\prompts1b\\groundtruth\\0rtt'
    elif packet_type == 'versionnego':
        expected_dict = expected_values["Version Negotiation Packet"]
        directory = 'input\\prompts1b\\groundtruth\\versionnego'
    elif packet_type == '1rtt':
        expected_dict = expected_values["1-RTT Packet"]
        directory = 'input\\prompts1b\\groundtruth\\1rtt'
    else:
        print('Error: packet_type incorrect')
        return
    
    seq_match_counter_list = []
    fv_match_counter_list = []

    #Iterate through each input
    for i, dict in enumerate(dict_list):
        # print('Iteration: ', i, '\n\t', dict)
        
        #Get number of fields in dictionary
        num_fields = len(dict)
        num_fields_list.append(num_fields)

        #Get missing field values
        expected_keys = set(expected_dict.keys())
        gpt_keys = set(dict.keys())
        missing_fields = expected_keys - gpt_keys
        # print('missing_fields are: ', missing_fields) 
        missing_fields_list.append(len(missing_fields))

        #Get hallucination matches
        hallucinate_fields = gpt_keys - expected_keys
        hallucinated_fields_list.append(len(hallucinate_fields))

        #Get matching field value pairs
        gt_file = f'{i+1}.txt'
        file_path = os.path.join(directory, gt_file) #Open ground truth file

        #Store ground truth file as a dictionary
        try:
            with open(file_path, 'r') as file:
                # Process the file as needed
                lines = file.readlines()
                gt_dict = {}
                for line in lines:
                    # parts = line.strip().split(':')
                    key, value = [part.strip() for part in line.split(':', 1)]
                    gt_dict[key] = value
                
                # print('Ground truth dict:\n\t', gt_dict, '\nGpt dict:\n\t', dict)

                #Compare to see if sequence matches and correct field value pairs
                seq_match_counter = 0
                keys2 = list(dict.keys()) #Gpt keys
                keys1 = list(gt_dict.keys()) #Ground truth keys
                fv_match_counter = 0

                # Iterate through the keys
                for i, (key1, key2) in enumerate(zip(keys1, keys2)):
                    # print(f"Iteration #{i}:")
                    # print(f"\t{key1} matching with {key2}")
                    
                    # Check if the keys match
                    if key1 == key2:
                        # print(f"\tKeys match: {key1}")
                        seq_match_counter += 1
                    
                    #Check if values match
                    if str(gt_dict[key1]) == str(dict[key2]):
                        # print(f"  Values match: {dict[key2]}")
                        fv_match_counter += 1
                    # else: print(f"  Values do not match: {gt_dict[key1]} (dict1) vs {dict[key2]} (dict2)")
                
                seq_match_counter_list.append(seq_match_counter)
                fv_match_counter_list.append(fv_match_counter)
                # print('fv_match counter list appending...', fv_match_counter_list)

        except FileNotFoundError:
            print(f"File {gt_file} not found.")

    #Calculate average fields
    print('DEBUGGING: num_fields_list: ', num_fields_list, len(num_fields_list), sum(num_fields_list))
    avg_num_fields = sum(num_fields_list)/len(num_fields_list)
    print('Average num fields is:', avg_num_fields)

    #Calculate missing fields
    print('\nDEBUGGING: Missing fields list: ', missing_fields_list)
    avg_missing = sum(missing_fields_list)/len(missing_fields_list) #Get average
    print('Missing fields (avg): ', avg_missing)
    # rate_missing = sum(missing_fields_list)/sum(num_fields_list) #Get rate
    # print('Missing fields (rate): ', rate_missing*100)

    #Calculate hallucinations
    print('\nDEBUGGING: Hallucinated fields: ', hallucinated_fields_list, len(hallucinated_fields_list), sum(hallucinated_fields_list))
    avg_hallucinate = sum(hallucinated_fields_list)/len(hallucinated_fields_list) #Average
    # rate_hallucinate = sum(hallucinated_fields_list)/sum(num_fields_list) #Rate
    print('Hallucinated fields (avg): ', avg_hallucinate)
    # print('Hallucinated fields (rate): ', rate_hallucinate*100)

    #Calculate sequence
    print('\nDEBUGGING: seq_match_list: ', seq_match_counter_list)
    avg_sequence = sum(seq_match_counter_list)/len(seq_match_counter_list) #Average
    # rate_sequence = sum(seq_match_counter_list)/sum(num_fields_list)
    print('Sequence matching (avg): ', avg_sequence)
    # print('Sequence matching (rate): ', rate_sequence*100)

    #Correct matching field value pairs
    print('\nDEBUGGING: fv_match_list: ', fv_match_counter_list)
    avg_matching_fv = sum(fv_match_counter_list)/len(fv_match_counter_list)
    # rate_matching_fv = sum(fv_match_counter_list)/sum(num_fields_list)
    print('Matching field values (avg): ', avg_matching_fv)
    # print('Matching field values (rate): ', rate_matching_fv*100)

# count_fields(initial_list, 'initial')
count_fields(zero_rtt_list, '0rtt')
# count_fields(handshake_list, 'handshake')
# count_fields(retry_list, 'retry')
# count_fields(versionnego_list, 'versionnego')
# count_fields(one_rtt_list, '1rtt')