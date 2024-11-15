#Evaluations for prompt 1a part 2
import os
import re
import matplotlib.pyplot as plt
from functions1a import *

path = 'input\\prompts1a\\all'
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

# Print the results
field_count_version = []
field_count_initial = []
field_count_0rtt = []
field_count_handshake = []
field_count_retry = []
field_count_1rtt = []

header_count_version = {}
header_count_initial = {}
header_count_0rtt = {}
header_count_handshake = {}
header_count_retry = {}
header_count_1rtt = {}

list_missing_fields = []
list_hallucinations = []
list_similarities = []

header_miss_version = []
header_miss_initial = []
header_miss_0rtt = []
header_miss_handshake = []
header_miss_retry = []
header_miss_1rtt = []

header_match_version = []
header_match_initial = []
header_match_0rtt = []
header_match_handshake = []
header_match_retry = []
header_match_1rtt = []

field_value_pair = {}
field_value_expected = {}

debug_label_count_initial = 0


#Put all inputs into files vector
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    
    # Reading in each file
    with open(filepath, "r") as file:
        #Remove opening line from file
        # file.readline()
        
        lines = file.readlines()

        packetname_leftover = ""

        for line in lines:
            #Skip empty spaces and skip lines that do not have 'packet' in its name
            if not line.strip(): continue
            if "packet" not in line.lower(): 
                # print(line, "not used")
                continue
            
            # print('DEBUGGING LINE:', line)

            # Check if the line contains curly braces
            if '{' in line and '}' in line:
                # Extract the part before the opening curly brace
                label, brace_content = line.split('{', 1)

                # Remove trailing whitespace and semicolon from the label
                label = label.strip().rstrip(':')
                # print(f'Checking if {label} matches with {packetname_leftover}')

                #Check for boundary cases with output file
                if (label != packetname_leftover):
                    # Add label from previous line and set leftover back to nothing
                    label = packetname_leftover + label

                    #If label is short hand packet rename it to 1-rtt packet
                    if label == "Short Header Packet": label = "1-RTT Packet"
                    if label == "Initial Packet": 
                        debug_label_count_initial += 1
                        # print('\tInitial packet!')
                packetname_leftover = ""
                
                # Extract the content inside the curly braces
                content = brace_content.split('}')[0]

                # Remove \r and \n values from items
                content = content.replace('\\r', '').replace('\\n', '').replace('\\', '')
                # print(content)

                # Split the content into individual items and remove \r and \n
                items = [item.strip() for item in content.split(',') if item.strip()]

                # Append the label and items to the files list
                files.append((label.strip(), items))
                # if label == "1-RTT Packet": print(f'\tAppended "{label.strip()}" with {items}\n')
                # for item in items:
                #     # print(item)
                #     if item == '160)': print(item)
            
            else:
                # Remove semicolon from line
                line = line.strip().rstrip(':')
                packetname_leftover = line
                # print("This has no {}", packetname_leftover)

# print('Initial packet count debug:', debug_label_count_initial)

for packet_type, packet in files:
    # print('Debugging opening for loop: ', packet_type)
    # if(packet_type == '1-RTT Packet'): print(f"DEBUGGING RESULTS: {packet_type}\n{packet}")
    if (packet_type in expected_values):
        # print(f"DEBUGGING: Matches ({packet_type})")
        expected_packet_dict = expected_values[packet_type]

        #Convert output into a dictionary
        try:
            packet_dict = dictconversion(packet)
        
        #If output is not formatted properly, mark as failed
        except (IndexError, ValueError) as e:
            print(f"ERRROR: Output packet not formatted properly: {e}")
            continue

        # print('DEBUGGING DICTIONARY:\n\t', packet_dict, '\nTRUE RESULT:\n\t', expected_packet_dict)

        #Get the keys from both dictionaries
        keys = packet_dict.keys()
        values = packet_dict.values()
        expected_keys = expected_packet_dict.keys()
        expected_vals = expected_packet_dict.values()

        # print(f'keys: {keys}\nvalues: {values}\nexpected keys: {expected_keys}\nexpected values: {expected_vals}\n')
        # Evaluation metric 5, matching field values (see eval2)
        # print(f'DEBUGGING packet_value_match:\n\tKeys:{keys}\n\tExpected keys:{expected_keys},\n\tValues:{values},\n\tExpected values:{expected_vals}')
        # print(f'Appending the following: ({packet_type}, ({keys}, {expected_keys}))')
        if packet_type not in field_value_pair:
            field_value_pair[packet_type] = []
        if packet_type not in field_value_expected:
            field_value_expected[packet_type] = []
        
        field_value_pair[packet_type].append((keys,values))
        field_value_expected[packet_type].append((expected_keys, expected_vals))

        # print(f'{(packet_type)} DEBUGGING: \nDictionary comparison', keys, '\n\n with expected keys: ', expected_keys)

        #Evaluation metric 0, overview of keys
        for key in keys:
            # if packet_type == "1-RTT Packet": print('DEBUGGING eval metric 0 key: ', key)
            match packet_type:
                case "Version Negotiation Packet":
                    # print('Version nego')
                    if key not in header_count_version:
                        header_count_version[key] = 0
                    header_count_version[key] += 1
                            
                case "Initial Packet":
                    if key not in header_count_initial:
                        header_count_initial[key] = 0
                    header_count_initial[key] += 1

                case "0-RTT Packet":
                    # print('Rtt')
                    if key not in header_count_0rtt:
                        header_count_0rtt[key] = 0
                    header_count_0rtt[key] += 1

                case "Handshake Packet":
                    # print('Handshake')
                    if key not in header_count_handshake:
                        header_count_handshake[key] = 0
                    header_count_handshake[key] += 1

                case "Retry Packet":
                    # print('Retry')
                    if key not in header_count_retry:
                        header_count_retry[key] = 0
                    header_count_retry[key] += 1
                
                case "1-RTT Packet": 
                    if key not in header_count_1rtt:
                        header_count_1rtt[key] = 0
                        # print('\n\n\tDebugging 1-rtt packet, adding header: ', key, '\n\n')
                    header_count_1rtt[key] += 1
                    
                case _:
                    print(f'{key} not in expected fields')
                    continue
        
        #Evaluation metric 1, average # packet fields generated
        match packet_type:
            case "Version Negotiation Packet": field_count_version.append(len(keys))
            case "Initial Packet": field_count_initial.append(len(keys))
            case "0-RTT Packet": field_count_0rtt.append(len(keys))
            case "Handshake Packet": field_count_handshake.append(len(keys))
            case "Retry Packet": field_count_retry.append(len(keys))
            case "1-RTT Packet": field_count_1rtt.append(len(keys))
            case _:
                print(f'{key} not in expected fields')
                continue

        #Evaluation metric 2, finding missing fields
        # print(f'Debugging eval metric 1\n\t{keys}')
        count_miss = miss_hallu_count(expected_keys, keys, 'Missing') #This function gets # of missing/hallucinated fields
        # print('Count miss:', count_miss)
        list_missing_fields.append((packet_type, count_miss))

        #Evaluation metric 3, finding hallucinations
        # print(f'Debugging eval metric 2\n\t{expected_keys}')
        count_hallu = miss_hallu_count(keys, expected_keys, 'Hallucinated')
        list_hallucinations.append((packet_type, count_hallu))
        
        #Evaluation metric 4, matching field names
        field = [re.sub(r'\s*\(.*?\)', '', item) for item in keys]
        expected_field = [re.sub(r'\s*\(.*?\)', '', item) for item in expected_keys]

        for key in expected_field:
            if key not in field:
                # if(packet_type=='Retry Packet'): print(f'{key} not in input, [{packet_type}]')

                #Append missing key to the matching packet
                match packet_type:
                    case "Version Negotiation Packet": header_miss_version.append(key)
                    case "Initial Packet": header_miss_initial.append(key)
                    case "0-RTT Packet": header_miss_0rtt.append(key)
                    case "Handshake Packet": header_miss_handshake.append(key)
                    case "Retry Packet": header_miss_retry.append(key)
                    case "1-RTT Packet": header_miss_1rtt.append(key)
                    case _:
                        print(f'{key} not in expected fields')
                        continue
            
            else: #Check for matching field names
                match packet_type:
                    case "Version Negotiation Packet": header_match_version.append(key)
                    case "Initial Packet": header_match_initial.append(key)
                    case "0-RTT Packet": header_match_0rtt.append(key)
                    case "Handshake Packet": header_match_handshake.append(key)
                    case "Retry Packet": header_match_retry.append(key)
                    case "1-RTT Packet": header_match_1rtt.append(key)
                    case _:
                        print(f'{key} not in expected fields')
                        continue

        #Evaluation metric 5, sequence matching < Commented out to see if this is needed. Delete if unused
        # similarity_ratio = SequenceMatcher(None, field, expected_field).ratio() #Using similarity ratio
        # list_similarities.append((packet_type, similarity_ratio))

    else:
        # print(f"ERROR: No expected values defined for packet type: {packet_type}")
        continue

#Plot and save bar graphs
output_dir = "output/evaluation"
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

#Evaluation 0 graphs
# print('initial', header_count_initial, sum(header_count_initial.values()), '\n')
# print('0rtt', header_count_0rtt, sum(header_count_0rtt.values()), '\n')
# print('handshake', header_count_handshake, sum(header_count_handshake.values()), '\n')
# print('retry', header_count_retry, sum(header_count_retry.values()), '\n')
# print('1rtt', header_count_1rtt, sum(header_count_1rtt.values()), '\n')
plot_overview_graph(header_count_initial, 'Grammar of ChatGPT-4o generated Initial packets', 'packet_count_initial')
plot_overview_graph(header_count_retry, 'Grammar of ChatGPT-4o generated Retry packets', 'packet_count_retry')
plot_overview_graph(header_count_0rtt, 'Grammar of ChatGPT-4o generated 0-RTT packets', 'packet_count_0rtt')
plot_overview_graph(header_count_version, 'Grammar of ChatGPT-4o generated Version Negotiation packets', 'packet_count_version')
plot_overview_graph(header_count_handshake, 'Grammar of ChatGPT-4o generated Handshake packets', 'packet_count_handshake')
plot_overview_graph(header_count_1rtt, 'Grammar of ChatGPT-4o generated 1-RTT packets', 'packet_count_1rtt')

#Evaluation 1: # Packet count
filepath = os.path.join(output_dir, 'Eval_tables.txt')
num_initial_packets = len(field_count_initial)
num_0rtt_packets = len(field_count_0rtt)
num_handshake_packets = len(field_count_handshake)
num_retry_packets = len(field_count_retry)
num_1rtt_packets = len(field_count_1rtt)

with open(filepath, 'w') as file:
    file.write(f"Average # packet fields generated:\n\tInitial: {sum(field_count_initial)/num_initial_packets}\n")
    file.write(f"\t0rtt: {sum(field_count_0rtt)/num_0rtt_packets}\n")
    file.write(f"\tHandshake: {sum(field_count_handshake)/num_handshake_packets}\n")
    file.write(f"\tRetry: {sum(field_count_retry)/num_retry_packets}\n")
    file.write(f"\t1-RTT: {sum(field_count_1rtt)/num_1rtt_packets}\n")

print('Initial Packet count:', field_count_initial, '\n Has average: ', sum(field_count_initial)/len(field_count_initial))
print('\n0rtt Packet count:', field_count_0rtt, '\n Has average: ', sum(field_count_0rtt)/len(field_count_0rtt))
print('\nHandshake Packet count:', field_count_handshake, '\n Has average: ', sum(field_count_handshake)/len(field_count_handshake))
print('\nRetry count:', field_count_retry, '\n Has average: ', sum(field_count_retry)/len(field_count_retry))

#Evaluation 2: Missing fields
# print('List missing fields:', list_missing_fields)
output_miss_hallu_seq(list_missing_fields, 'Missing')

#Evaluation 3: Hallucinations
# print('List hallucinations:', list_hallucinations)
output_miss_hallu_seq(list_hallucinations, 'Hallucination')

#Evaluation 4: Matching fields + field value pair
packet_value_match(field_value_pair, field_value_expected, num_initial_packets, num_0rtt_packets, num_handshake_packets, num_retry_packets, num_1rtt_packets)

#Evaluation 5: Sequence
packet_value_seq(field_value_pair, field_value_expected, num_initial_packets, num_0rtt_packets, num_handshake_packets, num_retry_packets, num_1rtt_packets)
