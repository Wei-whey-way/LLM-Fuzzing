import re

# Given dictionary
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

# Given string
packet_string = "Retry Packet: {Header Form (1): 0x0, Fixed Bit (1): 0x1, Long Packet Type (2): 0x3, Unused (4): <Value>, Version (32): <Value>, Destination Connection ID Length (8): <Value>, Destination Connection ID (0..160): <Value>, Source Connection ID Length (8): <Value>, Source Connection ID (0..160): <Value>, Retry Token (..): <Value>, Retry Integrity Tag (128): <Value>}"

# Extract packet type and properties part
packet_type, properties = re.match(r"([^:]+): (.+)", packet_string).groups()
properties = properties.strip('{}')
# print(packet_type)
# print(properties)

# Split properties further by comma and construct a dictionary
property_dict = {}
for prop in properties.split(','):
    key, value = prop.split(':', 1)
    property_dict[key.strip()] = value.strip()

# print('DEBUG input test:\n', property_dict)

# Matching the format with expected_values
if packet_type in expected_values:
    expected_packet_values = expected_values[packet_type]
    print('DEBUG: Packet type:\n', packet_type)
    for key in expected_packet_values:
        print(f"DEBUG MATCHING: {key}\n{value.strip()} with {expected_packet_values[key]}")
        if value.strip() != expected_packet_values[key]:
            print(f"Mismatch in property '{key}': Expected '{expected_packet_values[key]}', Got '{value}'")
        else:
            print("DEBUG: VALUES MATCH") 
else:
    print("Packet name not found in expected_values")