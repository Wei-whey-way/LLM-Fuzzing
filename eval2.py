import os
import re
import matplotlib.pyplot as plt

path = 'output\\packettest'
files = []

def extract_packet_info(line):
    # Define the regular expression pattern to match the packet type and values inside curly braces
    pattern = r"{(.*?)}"
    matches = re.findall(pattern, line)
    if matches:
        return matches[0]  # return the first match
    return None

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
    
    #Reading in output file
    with open(filepath, "r") as file:
        input = file.readlines()

        #Preprocessing
        for line in input:
            input = line.split('{')[-1].replace('}', '').split(',')
        # input = [line.replace('\n', '').replace('\r','').replace('\\r','').replace('\\n','') for line in input if line.strip()]
        files.append(input)

#Getting packet information
for i, packet_list in enumerate(files):
    print(f"DEBUG File: {i+1}\n{packet_list}\n\n")
    
    # Extract packet type and properties part
    for packet in packet_list[1:]:
        print("DEBUG PACKET LOOPS\n", packet)
        # print(type(packet))
        # packet_type, properties = re.match(r"([^:]+): (.+)", packet).groups()
        # properties = properties.strip('{}')
        # print(properties)
    
    #Iterate over each line and extract packet info
    for line in packet_list:
        packet_type = None
        if "Version Negotiation Packet" in line:
            packet_type = "Version Negotiation Packet"
        elif "Initial Packet" in line:
            packet_type = "Initial Packet"
        elif "0-RTT Packet" in line:
            packet_type = "0-RTT Packet"
        elif "Handshake Packet" in line:
            packet_type = "Handshake Packet"
        elif "Retry Packet" in line:
            packet_type = "Retry Packet"
        
        if packet_type:
            packet_info = extract_packet_info(line)
            # print("DEBUG:\n",packet_info)
            if (packet_info is not None):
                expected_info = expected_values.get(packet_type, {})
                # print("DEBUG:\n", expected_info)
                # if packet_info != expected_info:
                #     print(f"Mismatched packets ({packet_type})\nInput:{packet_info},\nExpected:{expected_info}\n")
                #     mismatched_packets.append((packet_type, packet_info, expected_info))
