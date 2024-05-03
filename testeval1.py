import re

# Define the function to compare actual values with expected values
def compare_packet_info(packet_type, expected_info, packet_info):
    mismatches = []
    for key, expected_value in expected_info.items():
        if key not in packet_info or packet_info[key] != expected_value:
            mismatches.append((key, packet_info.get(key, ""), expected_value))
    return mismatches

def extract_packet_info(line):
    # Define the regular expression pattern to match the packet type and values inside curly braces
    pattern = r"{(.*?)}"
    matches = re.findall(pattern, line)
    if matches:
        return matches[0]  # return the first match
    return None

# Define the expected values for each packet type
expected_values = {
    "Version Negotiation Packet": {
        "Header Form (1)": "0x00",
        "Unused (7)": "<Value>",
        "Version (32)": "0x00",
        "Destination Connection ID Length (8)": "<Value>",
        "Destination Connection ID (0..2040)": "<Value>",
        "Source Connection ID Length (8)": "<Value>",
        "Source Connection ID (0..2040)": "<Value>",
        "Supported Version (32)": "<Value>",
    },
    "Initial Packet": {
        "Header Form (1)": "0x01",
        "Fixed Bit (1)": "0x01",
        "Long Packet Type (2)": "0x00",
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
        "Header Form (1)": "0x01",
        "Fixed Bit (1)": "0x01",
        "Long Packet Type (2)": "0x01",
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
        "Header Form (1)": "0x01",
        "Fixed Bit (1)": "0x01",
        "Long Packet Type (2)": "0x02",
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
        "Header Form (1)": "0x01",
        "Fixed Bit (1)": "0x01",
        "Long Packet Type (2)": "0x03",
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

# Sample input lines
lines = [
    "Initial Packet: {Header Form (1): 0x01, Fixed Bit (1): 0x01, Long Packet Type (2): 0x00}",
    "0-RTT Packet: {Header Form (1): 0x01, Fixed Bit (1): 0x01, Long Packet Type (2): 0x01}",
    "Handshake Packet: {Header Form (1): 0x01, Fixed Bit (1): 0x01, Long Packet Type (2): 0x02}",
    "Retry Packet: {Header Form (1): 0x01, Fixed Bit (1): 0x01, Long Packet Type (2): 0x03, Unused (4): <Value>, Version (32): <Value>, Destination Connection ID Length (8): <Value>, Destination Connection ID (0..160): <Value>, Source Connection ID Length (8): <Value>, Source Connection ID (0..160): <Value>, Retry Token (..): <Value>, Retry Integrity Tag (128): <Value>}",
]

# Initialize a list to store mismatched packets
mismatched_packets = []

# Iterate over each line and extract packet info
for line in lines:
    packet_type = None
    for expected_packet_type, expected_info in expected_values.items():
        if expected_packet_type in line:
            packet_type = expected_packet_type
            break
    
    if packet_type:
        packet_info = extract_packet_info(line)
        if packet_info is not None:
            # Check if extracted values match the expected values
            expected_info = expected_values.get(packet_type, {})
            
            mismatches = compare_packet_info(packet_type, expected_info, packet_info)