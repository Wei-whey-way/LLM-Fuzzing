#File to create batch prompt format for prompts 1b. Run this code after running task1b_extractor
import os
from pathlib import Path
import json

bytestream_dir = 'input/prompts1b'
output_dir = 'input/batchinputprompts'
# valid_files = ['binary_extractor_initial.txt', 'binary_extractor_0rtt.txt', 'binary_extractor_handshake.txt', 'binary_extractor_retry.txt']

#Make output folder
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if os.path.exists('input/batchinputprompts/1b-batchprompts-initial'): os.remove('input/batchinputprompts/1b-batchprompts-initial')
if os.path.exists('input/batchinputprompts/1b-batchprompts-handshake'): os.remove('input/batchinputprompts/1b-batchprompts-handshake')
# if os.path.exists('input/prompts1b/binary_extractor_0rtt.txt'): os.remove('input/prompts1b/binary_extractor_0rtt.txt')
if os.path.exists('input/batchinputprompts/1b-batchprompts-retry'): os.remove('input/batchinputprompts/1b-batchprompts-retry')
if os.path.exists('input/batchinputprompts/1b-batchprompts-versionnego'): os.remove('input/batchinputprompts/1b-batchprompts-versionnego')
if os.path.exists('input/batchinputprompts/1b-batchprompts-1rtt'): os.remove('input/batchinputprompts/1b-batchprompts-1rtt')


#Function to extract hex string from files
def hex_extract(file_location):
    hex_list = []

    if file_location.is_file():
        file = open(file_location, 'r')
        for line in file:
            line = line.split(': ') #Get only the hexstream from prompts1a
            hexstream = line[1]
            # print(hexstream)
            hex_list.append(hexstream)
        file.close()

    return hex_list

#Create prompts
def generate_batch_prompt(packet_name, bytestream, i, model):
    # id = "request-" + str(i)
    # print(id)
    prompt = "This is the RFC 9000, QUIC packet documentation: https://www.rfc-editor.org/rfc/rfc9000.html. "

    match packet_name:
        case 'initial':
            prompt += "And this is the Initial Packet from the documentation: \n\n\"Initial Packet\": { \"Header Form (1)\": \"0x1\", \"Fixed Bit (1)\": \"0x1\", \"Long Packet Type (2)\": \"0x0\", \"Reserved Bits (2)\": \"<Value>\", \"Packet Number Length (2)\": \"<Value>\", \"Version (32)\": \"<Value>\", \"Destination Connection ID Length (8)\": \"<Value>\", \"Destination Connection ID (0..160)\": \"<Value>\", \"Source Connection ID Length (8)\": \"<Value>\", \"Source Connection ID (0..160)\": \"<Value>\", \"Token Length (i)\": \"<Value>\", \"Token (..)\": \"<Value>\", \"Length (i)\": \"<Value>\", \"Packet Number (8..32)\": \"<Value>\", \"Packet Payload (8..)\": \"<Value>\", } \n\nFrom the following hex string, place all the values correctly into the Initial packet. \n\nBytestream: "
    
        case 'handshake':
            prompt += "And this is the Handshake Packet from the documentation: \n\n\"Handshake Packet\": { \"Header Form (1)\": \"0x1\", \"Fixed Bit (1)\": \"0x1\", \"Long Packet Type (2)\": \"0x0\", \"Reserved Bits (2)\": \"<Value>\", \"Packet Number Length (2)\": \"<Value>\", \"Version (32)\": \"<Value>\", \"Destination Connection ID Length (8)\": \"<Value>\", \"Destination Connection ID (0..160)\": \"<Value>\", \"Length (i)\": \"<Value>\", \"Packet Number (8..32)\": \"<Value>\", \"Packet Payload (8..)\": \"<Value>\"} \n\nFrom the following hex string, place all the values correctly into the Handshake packet. \n\nBytestream: "
    
        case 'retry':
            prompt += "And this is the Retry Packet from the documentation: \n\n\"Retry Packet\": { \"Header Form (1)\": \"0x1\", \"Fixed Bit (1)\": \"0x1\", \"Long Packet Type (2)\": \"0x0\", \"Unused (4)\": \"<Value>\", \"Version (32)\": \"<Value>\", \"Destination Connection ID Length (8)\": \"<Value>\", \"Destination Connection ID (0..160)\": \"<Value>\", \"Source Connection ID Length (8)\": \"<Value>\", \"Source Connection ID (0..160)\": \"<Value>\", \"Retry Token (..)\": \"<Value>\", \"Retry Integrity Tag (128)\": \"<Value>\"} \n\nFrom the following hex string, place all the values correctly into the Retry packet. \n\nBytestream: "
        
        case 'versionnego':
            prompt += "And this is the Version Negotation Packet from the documentation: \n\n\"Version Negotiation Packet\": { \"Header Form (1)\": \"0x1\", \"Unused (7)\": \"<Value>\", \"Version (32)\": \"<Value>\", \"Destination Connection ID Length (8)\": \"<Value>\", \"Destination Connection ID (0..2040)\": \"<Value>\", \"Source Connection ID Length (8)\": \"<Value>\", \"Source Connection ID (0..2040)\": \"<Value>\", \"Supported Version (32)\": \"<Value>\" } \n\nFrom the following hex string, place all the values correctly into the Version Negotiation packet. \n\nBytestream: "
        
        case '0rtt':
            prompt += "And this is the 0-RTT Packet from the documentation: \n\n\"0-RTT Packet\": { \"Header Form (1)\": \"0x1\", \"Fixed Bit (1)\": \"0x1\", \"Long Packet Type (2)\": \"0x0\", \"Reserved Bits (2)\": \"<Value>\", \"Packet Number Length (2)\": \"<Value>\", \"Version (32)\": \"<Value>\", \"Destination Connection ID Length (8)\": \"<Value>\", \"Destination Connection ID (0..160)\": \"<Value>\", \"Source Connection ID Length (8)\": \"<Value>\", \"Source Connection ID (0..160)\": \"<Value>\", \"Length (i)\": \"<Value>\", \"Packet Number (8..32)\": \"<Value>\", \"Packet Payload (8..)\": \"<Value>\" } \n\nFrom the following hex string, place all the values correctly into the 0-RTT packet. \n\nBytestream: "
        
        case '1rtt':
            prompt += "And this is the 1-RTT Packet from the documentation: \n\n\"1-RTT Packet\": { \"Header Form (1)\": \"0x1\", \"Fixed Bit (1)\": \"0x1\", \"Spin Bit (1)\": \"<Value>\", \"Reserved Bits (2)\": \"<Value>\", \"Key Phase (1)\": \"<Value>\", \"Packet Number Length (2)\": \"<Value>\", \"Destination Connection ID (0..160)\": \"<Value>\", \"Packet Number (8..32)\": \"<Value>\", \"Packet Payload (8..)\": \"<Value>\" } \n\nFrom the following hex string, place all the values correctly into the 1-RTT packet. \n\nBytestream: "
        
        # case '_':
    prompt += bytestream
    prompt += "\n\nGive only the answer in the above format."

    token_length = int(len(prompt)/4 + 1140) #500 originally still not enough

    batch_prompt = {"custom_id": "request-"+str(i), 
                    "method": "POST", 
                    "url": "/v1/chat/completions", 
                    "body": {"model": model, 
                             "messages": [
                                 {"role": "system", 
                                  "content": prompt
                                  }],
                                  "max_tokens": token_length}}
    
    return batch_prompt

#Put all inputs into files vector
initial_file = Path('input/prompts1b/raw_hex_list/binary_extractor_initial.txt')
hex_str_ini = hex_extract(initial_file)
# print(hex_str_ini)

zerortt_file = Path('input/prompts1b/raw_hex_list/binary_extractor_0rtt.txt')
hex_str_0rtt = hex_extract(zerortt_file)
# print(len(hex_str_0rtt))

retry_file = Path('input/prompts1b/raw_hex_list/binary_extractor_retry.txt')
hex_str_ret = hex_extract(retry_file)

handshake_file = Path('input/prompts1b/raw_hex_list/binary_extractor_handshake.txt')
hex_str_hs = hex_extract(handshake_file)

versionnego_file = Path('input/prompts1b/raw_hex_list/binary_extractor_versionnego.txt')
hex_str_vn = hex_extract(versionnego_file)

onertt_file = Path('input/prompts1b/raw_hex_list/binary_extractor_1rtt.txt')
hex_str_1rtt = hex_extract(onertt_file)

#Function to extract the raw batch files into the folder batchinputprompts
def output_batches(packet_name, file_name, hex_str):
    file = open(file_name, "w")
    for i, hex_str in enumerate(hex_str):
        # print(hex_str)
        prompt = generate_batch_prompt(packet_name, hex_str, i+1, "gpt-4o")
        # prompt = generate_batch_prompt(hex_str, i+1, "gpt-3.5-turbo-0125")
        file.write(json.dumps(prompt) + "\n")
    file.close()

    return

#Extract all prompts into separate batch prompts
#Version Negotiation packet
output_batches('versionnego', "input/batchinputprompts/1b-batchprompts-versionnego.jsonl", hex_str_vn)

#Initial packet
output_batches('initial', "input/batchinputprompts/1b-batchprompts-initial.jsonl", hex_str_ini)

#Handshake packet
output_batches('handshake', "input/batchinputprompts/1b-batchprompts-handshake.jsonl", hex_str_hs)

#0-rtt packet
# "input/batchinputprompts/1b-batchprompts-0rtt.jsonl": hex_str_0rtt

#Retry packet
output_batches('retry', "input/batchinputprompts/1b-batchprompts-retry.jsonl", hex_str_ret)

#1-rtt packet
output_batches('1rtt', "input/batchinputprompts/1b-batchprompts-1rtt.jsonl", hex_str_1rtt)


# file = open(file_name, "w")
# for i, hex_str in enumerate(hex_str_ini):
#     # print(hex_str)
#     prompt = generate_batch_prompt(hex_str, i+1, "gpt-3.5-turbo-0125")
#     file.write(json.dumps(prompt) + "\n")
# file.close()


# client = OpenAI()
# print("Now generating packets...")

# for i, line in enumerate(binary_list):
#     follow_up_prompt = generate_follow_up_prompt(line)

#     #Sending prompt to chatgpt
#     initial_message = {
#         "role": "system",
#         "content": f"{follow_up_prompt}"
#     }

#     #Extract prompts and 
#     prompt_path = os.path.join('output/mutablefield/output', f'mutable_prompt{i+1}.txt')

#     #Writing prompts to new file
#     with open(prompt_path, 'w') as file:
#         file.write(follow_up_prompt)

#     gpt_prompt = client.chat.completions.create(
#         model="gpt-4",
#         messages = [initial_message],
#         temperature=0.5,
#         max_tokens=1600,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )

#     #Extract prompts to output folder
#     prompt_path = os.path.join('output/mutablefield/output', f'mutable_prompt{i+1}.txt')
#     with open(prompt_path, 'w') as file:
#         file.write(follow_up_prompt)
    
#     #Extract chatgpt output to output folder
#     file_path = os.path.join('output/mutablefield/output', f'mutable_output{i+1}.txt')
#     output = str(gpt_prompt.choices[0].message.content)
#     with open(file_path, 'w') as file:
#         file.write(output)


# print("Testing complete")
