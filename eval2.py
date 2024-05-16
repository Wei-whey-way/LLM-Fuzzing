import os
import re
import matplotlib.pyplot as plt

path = 'output\\packettest'
files = []

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
    # print(f"DEBUGGING RESULTS: {packet_type}\n\t {packet} \n")
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

        # print('DEBUGGING DICTIONARY:', packet_dict)

        #Get the keys from both dictionaries to check if values match
        keys = expected_packet_dict.keys()
        # print('DEBUGGING: Dictionary comparison', keys)
        
        correct_match = True
        for key in keys:
            value1 = packet_dict.get(key)
            value2 = expected_packet_dict.get(key)
            # print(f'\t{value1} comparing with {value2}')
            
            if(value1 != value2):
                fail_count += 1
                # print(f'\tValues mismatch. {key}: {value1} should be {value2}')
                correct_match = False
                break
        
        if (correct_match == True):
            # print("\tAll values matched!")
            succ_count += 1
            packet_counters[packet_type] += 1
        # else:
            # print("\tPacket did not fully match")

    else:
        print(f"ERROR: No expected values defined for packet type: {packet_type}")

print(f'\nDEBUGGING FINAL COUNT:\n\t# packets fully matched: {succ_count}\n\t# failures: {fail_count}\n')
print("Number of packets successfully matched")
for packet in packet_counters:
    print(f'\t{packet}: {packet_counters[packet]}')

#Plot and save bar graphs
output_dir = "output/evaluation"
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

plt.bar(packet_counters.keys(), packet_counters.values())
plt.title("Packet Type Accuracy")
plt.xlabel("Packet Type")
plt.ylabel("# Successful matches")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "packet_type_successful_matches.png"))
plt.show()