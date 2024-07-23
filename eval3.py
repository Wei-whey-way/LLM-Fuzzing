import os
import re
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
nltk.download('punkt')

path = 'output\\packettest'
files = []

def parse_text(text):
    pairs = text.split(',')
    parsed_dict = {}
    for pair in pairs:
        # Trim whitespace from the beginning and end
        pair = pair.strip()
        if pair:
            # Split field and value
            field_value = pair.split(': ')
            if len(field_value) == 2:
                field = field_value[0].strip()
                value = field_value[1].strip('<> ')
                parsed_dict[field] = value
    
    return parsed_dict

def calculate_repetition_ratio(text1, text2):
    dict1 = parse_text(text1)
    dict2 = parse_text(text2)
    total_fields = len(dict1)
	# repeated_fields =
    for field in dict1:
        if field in dict2 and dict1[field] == dict2[field]:
            repeated_fields += 1
    repetition_ratio = repeated_fields / total_fields if total_fields > 0 else 0
    
    return repetition_ratio

#Initialise counters
packet_counters = {
    "Version Negotiation Packet": 0,
    "Initial Packet": 0,
    "0-RTT Packet": 0,
    "Handshake Packet": 0,
    "Retry Packet": 0,
}

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
        "Destination Connection ID Len (8)": "<Value>",
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
        "Destination Connection ID Len (8)": "<Value>",
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
    }
}

#Put all inputs into files vector
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    
    # Reading in each file
    with open(filepath, "r") as file:
        #Remove opening line from file
        file.readline()
        
        lines = file.readlines()

        packetname_leftover = ""

        for line in lines:            
            #Skip empty spaces
            if not line.strip(): 
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
                # print(f'\tAppended "{label.strip()}" with {items}')
            
            else:
                # Remove semicolon from line
                line = line.strip().rstrip(':')
                packetname_leftover = line
                # print("This has no {}", packetname_leftover)


succ_count = 0
fail_count = 0

#Initialize counters
packet_counters = {
    "Version Negotiation Packet": 0,
    "Initial Packet": 0,
    "0-RTT Packet": 0,
    "Handshake Packet": 0,
    "Retry Packet": 0,
}

# Print the results
for packet_type, packet in files:
    # print('\n',packet_type)
    # print(f"DEBUGGING RESULTS: {packet_type}\n\t {packet} \nTRUE RESULT: \n\t{expected_values[packet_type]}")
    if (packet_type in expected_values):
        # print("DEBUGGING: Matches")
        expected_packet_dict = expected_values[packet_type]

        #If length of packet mismatches, count it as error and go to next iteration
        if len(packet) != len(expected_packet_dict):
            # print(f"Packet length mismatch: {len(packet)} should be {len(expected_packet_dict)}")
            # print(packet, '\n', expected_packet_dict)
            fail_count += 1
            continue

        #Convert output into a dictionary
        packet_dict = {}
        try:
            for item in packet:
                # Split each item at the colon (':')
                key_value_pair = item.split(':')
                key = key_value_pair[0].strip()
                value = key_value_pair[1].strip()
                
                # Add the key-value pair to the dictionary
                packet_dict[key] = value
        
        #If output is not formatted properly, mark as failed
        except (IndexError, ValueError) as e:
            print(f"ERRROR: Output packet not formatted properly: {e}")
            fail_count += 1
            continue

        # print('DEBUGGING DICTIONARY:\n\t', packet_dict, '\nTRUE RESULT:\n\t', expected_packet_dict)

        #Get the keys from both dictionaries
        # print(packet_dict, '\n', packet_dict.keys())
        keys = packet_dict.keys()
        expected_keys = expected_packet_dict.keys()
        # print('DEBUGGING: Dictionary comparison', keys, '\n with expected keys: ', expected_keys)
        
        #Evaluation metric 1, finding missing fields
        # print(f'Debugging eval metric 1\n\t{keys}')
        count_miss = 0
        for key in expected_keys:
            # print('\t', key)
            if key not in keys:
                print(f"key {key} is a missing field\n")
                count_miss += 1
        
        rate_miss = count_miss / len(expected_keys)
        
        #Evaluation metric 2, finding hallucinations
        count_hallu = 0
        # print(f'Debugging eval metric 2\n\t{expected_keys}')
        for key in keys:
            if key not in expected_keys:
                print(f"key {key} is a missing field\n")
                count_hallu += 1
        
        rate_hallu = count_hallu / len(keys)
        
        #Evaluation metric 3, matching fields ()
        #Convert words into lowercase
        text1 = ' '.join(keys)
        text2 = ' '.join(expected_keys)
        # print('text1:', text1)
        words1 = [word.lower() for word in word_tokenize(text1)]
        words2 = [word.lower() for word in word_tokenize(text2)]
        # print('words2:', words2, len(words2))

        #Count word frequency
        counter1 = Counter(words1)
        counter2 = Counter(words2)
        # print('\tCounter\n', counter1)

        # Get matching rate
        repeated_words = set(counter1) & set(counter2)
        # print(len(repeated_words), 'compared with', len(words2))
        matching_rate = len(repeated_words)/len(words2)
        # print('AAAAAA\n', repeated_words, len(repeated_words))
        print('matching rate:', matching_rate)

        #Evaluation metric 4, matching field values (see eval2)
        
    else:
        print(f"ERROR: No expected values defined for packet type: {packet_type}")