import os
import re
import matplotlib.pyplot as plt

path = 'output\\packettest'
files = []

def extract_packet_info(line):
    #Define the regular expression pattern to match the packet type and values inside curly braces
    pattern = r"{(.*?)}"
    matches = re.findall(pattern, line)
    if matches:
        return matches[0]  # return the first match
    return None

#Initialize counters
packet_counters = {
    "Version Negotiation Packet": 0,
    "Initial Packet": 0,
    "0-RTT Packet": 0,
    "Handshake Packet": 0,
    "Retry Packet": 0,
}

#Put all inputs into files vector
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    
    #Reading in output file
    with open(filepath, "r") as file:
        input = file.readlines()

        #Preprocessing
        input = [line.replace('\n', '').replace('\r','').replace('\\r','').replace('\\n','') for line in input if line.strip()]
        files.append(input)

#Getting packet information
for i, vector in enumerate(files):
    # print(f"File: {i+1}\n{vector}\n\n")
    
    #Iterate over each line and extract packet info
    for line in vector:
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
            if (packet_info is not None):
                print(f"{packet_type}: {packet_info}\n")
                packet_counters[packet_type] += 1

# #Print packet counters
# for packet_type, count in packet_counters.items():
#     print(f"{packet_type} count: {count}")

#Plot and save bar graphs
output_dir = "output/evaluation"
os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

plt.bar(packet_counters.keys(), packet_counters.values())
plt.title("Packet Type Counts")
plt.xlabel("Packet Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
# plt.savefig(os.path.join(output_dir, "packet_type_counts.png"))
# plt.show()