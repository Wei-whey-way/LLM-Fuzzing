from openai import OpenAI
from dotenv import load_dotenv, dotenv_values 
import os

#Outlining process of what I did. I truncated Kai's hexadecimal bytestream to a length of 77 digits (if not it goes over hundreds of digits).
#Converted hexadecimal to binary

load_dotenv() 

# example_hex = 'cd0000000108da593d405edcaa7808be36c72621baa4730044e64c45d1ddb9f629c75680937dc'
# print(len(example_hex))

#Make output folder
if not os.path.exists('output'):
    os.makedirs('output')

if not os.path.exists('output/mutablefield'):
    os.makedirs('output/mutablefield')

if not os.path.exists('output/mutablefield/output'):
    os.makedirs('output/mutablefield/output')

path = 'output\\mutablefield\\inputs'

#Reading in file containing hexadecimal bytestream
for filename in os.listdir(path):
    filepath = os.path.join(path,filename)
    
    # Reading in file
    with open(filepath, "r") as file:
        #Read in each line
        lines = file.readlines()
        # for line in lines:
        #     print(line, '\n')

        binary_list = []

        #Read each line in hex bytestream input file and convert to binary
        for hex_line in lines:
            #Truncate line to length 77
            hex_line = (hex_line[:77]) if len(hex_line) > 77 else hex_line
            # print(hex_line)

            #Convert from hexadecimal to binary
            bin_line = bin(int(hex_line, 16)).zfill(8)
            bin_line = bin_line[2:] #Remove the 0b (from binary)
            # print(bin_line, type(bin_line))
            # print('aaaa')

            binary_list.append(bin_line)

        # print(binary_list)

#Create prompts
def generate_follow_up_prompt(bytestream):
    prompt = "This is the RFC 9000, QUIC packet documentation: https://www.rfc-editor.org/rfc/rfc9000.html. And this is the Version Negotiation Packet from the documentation: \n\n\"Initial Packet\": { \"Header Form (1)\": \"0x1\", \"Fixed Bit (1)\": \"0x1\", \"Long Packet Type (2)\": \"0x0\", \"Reserved Bits (2)\": \"<Value>\", \"Packet Number Length (2)\": \"<Value>\", \"Version (32)\": \"<Value>\", \"Destination Connection ID Len (8)\": \"<Value>\", \"Destination Connection ID (0..160)\": \"<Value>\", \"Source Connection ID Length (8)\": \"<Value>\", \"Source Connection ID (0..160)\": \"<Value>\", \"Token Length (i)\": \"<Value>\", \"Token (..)\": \"<Value>\", \"Length (i)\": \"<Value>\", \"Packet Number (8..32)\": \"<Value>\", \"Packet Payload (8..)\": \"<Value>\", } \n\nFrom the following binary string, place all the values correctly into the Initial packet. \n\nBytestream: "
    prompt += bytestream
    prompt += "\n\nGive only the answer in the above format"
    # print(prompt)

    return prompt

client = OpenAI()
print("Now generating packets...")

for i, line in enumerate(binary_list):
    follow_up_prompt = generate_follow_up_prompt(line)

    #Sending prompt to chatgpt
    initial_message = {
        "role": "system",
        "content": f"{follow_up_prompt}"
    }

    #Extract prompts and 
    prompt_path = os.path.join('output/mutablefield/output', f'mutable_prompt{i+1}.txt')

    #Writing prompts to new file
    with open(prompt_path, 'w') as file:
        file.write(follow_up_prompt)

    gpt_prompt = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [initial_message],
        temperature=0.5,
        max_tokens=1600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    #Extract prompts to output folder
    prompt_path = os.path.join('output/mutablefield/output', f'mutable_prompt{i+1}.txt')
    with open(prompt_path, 'w') as file:
        file.write(follow_up_prompt)
    
    #Extract chatgpt output to output folder
    file_path = os.path.join('output/mutablefield/output', f'mutable_output{i+1}.txt')
    output = str(gpt_prompt.choices[0].message.content)
    with open(file_path, 'w') as file:
        file.write(output)


print("Testing complete")
