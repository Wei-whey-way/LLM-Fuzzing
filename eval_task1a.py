#Evaluations for prompt1a part 1

import os
import re
import matplotlib.pyplot as plt
from collections import Counter

path = 'input\\prompts1a'
output_path = "output\\prompts1a"
files = []

if not os.path.exists("output\\prompts1a\\chatafl"): os.makedirs("output\\prompts1a\\chatafl")
if not os.path.exists("output\\prompts1a\\context"): os.makedirs("output\\prompts1a\\context")
if not os.path.exists("output\\prompts1a\\rag"): os.makedirs("output\\prompts1a\\rag")
if not os.path.exists("output\\prompts1a\\all"): os.makedirs("output\\prompts1a\\all")

# def extract_packet_info(line):
#     #Define the regular expression pattern to match the packet type and values inside curly braces
#     pattern = r"{(.*?)}"
#     matches = re.findall(pattern, line)
#     if matches:
#         return matches[0]  # return the first match
#     return None

# #Function to parse input text into a readable format
def parse_text_chatafl(promptpath):
    #Initialize counters
    packet_counters = {}
    
    for file in os.listdir(promptpath):
        filepath = os.path.join(promptpath,file)
        print('\t', filepath)
    
        #Reading in output file
        with open(filepath, "r") as file:
            output_file = filepath.replace('input','output')
            f = open(output_file, "w") 
            # print('output directory:', output_file)
            input = file.readlines()

            #Preprocessing + Cleaning up data
            # input = [line.replace('\n', '').replace('\r','').replace('\\r','').replace('\\n','') for line in input if line.strip()]
            input = [line for line in input if '`' not in line and 'shot' not in line.lower() and 'sure' not in line.lower() and line != '\n'] #Remove ` in line
            # print('Checking input', input)
            
            for line in input:
                line = line.strip().replace(',','').replace('-','')
                print('Checking:', line)
                # f.write(line + '\n')
                if "{" in line and "}" in line:
                    before_brace = line.split('{')[0].strip()  # Part before the curly brace
                    f.write(before_brace + '\n')
                    print('\tb4 brace:', before_brace)
                    
                    inner_content = line.split('{')[1].split('}')[0]
                    elements = inner_content.split(',')
                    print('\telements:', elements)

                    for element in elements:
                        f.write(element.strip() + '\n')
                        # print(element.strip())
                elif line.strip() == "{" or line.strip() == "}": pass
                elif "{" in line:
                    line = line.replace("{",'')
                    f.write(line + '\n')
                else:
                    f.write(line + '\n')
                
            # print(f)
            f.close()
    return

def parse_text_rag(promptpath):
    # print('rag')
    for file in os.listdir(promptpath):
        filepath = os.path.join(promptpath,file)
        print(filepath)
    
        #Reading in output file
        with open(filepath, "r") as file:
            output_file = filepath.replace('input','output')
            f = open(output_file, "w") 
            # print('output directory:', output_file)
            input = file.readlines()

            #Preprocessing + Cleaning up data
            # input = [line.replace('\n', '').replace('\r','').replace('\\r','').replace('\\n','') for line in input if line.strip()]
            input = [line for line in input if '`' not in line and 'shot' not in line.lower() and 'sure' not in line.lower() and line != '\n' and 'for the quic protocol' not in line.lower()] #Remove ` in line
            print('Checking input', input)
            
            for line in input:
                line = line.strip().replace(',','').replace('-','')
                print('Checking:', line)
                if line.count(":") == 2: #Split header line by two
                    first_part, rest_of_line = line.split(":", 1)  # Split only at the first semicolon
                    f.write(f"{first_part.strip()}:\n{rest_of_line.strip().replace("{","")}\n")
                    # print(f"\tFirst part: {first_part.strip()}:")
                    # print(f"\tRest of the line: {rest_of_line.strip()}")
                elif "{" in line and "}" in line:
                    before_brace = line.split('{')[0].strip()  # Part before the curly brace
                    f.write(before_brace + '\n')
                    # print('\tb4 brace:', before_brace)
                    
                    inner_content = line.split('{')[1].split('}')[0]
                    elements = inner_content.split(',')
                    # print('\telements:', elements)

                    for element in elements:
                        f.write(element.strip() + '\n')
                        # print(element.strip())
                elif line.strip() == "{" or line.strip() == "}": pass
                elif "{" in line:
                    line = line.replace("{",'')
                    f.write(line + '\n')
                else:
                    f.write(line + '\n')
                
            # print(f)
            f.close()

def parse_text_context(promptpath):
    print('context')
    for file in os.listdir(promptpath):
        filepath = os.path.join(promptpath,file)
        print(filepath)
    
        #Reading in output file
        with open(filepath, "r") as file:
            output_file = filepath.replace('input','output')
            f = open(output_file, "w") 
            # print('output directory:', output_file)
            input = file.readlines()

            #Preprocessing + Cleaning up data
            input = [line.replace('\n', '').replace('\r','').replace('\\r','').replace('\\n','') for line in input if line.strip()]
            input = [line for line in input if '`' not in line and 'shot' not in line.lower() and 'sure' not in line.lower() and 'certainly' not in line.lower() and 'please' not in line.lower() and 'refer' not in line.lower() and 'are' not in line.lower() and 'for the quic protocol' not in line.lower()] #Remove ` in line
            # if output_file == 'output\\prompts1a\\context\\output3.txt': print('Checking input', input)
            
            for line in input:
                line = line.strip().replace(',','').replace('-','')
                if output_file == 'output\\prompts1a\\context\output3.txt': print('Checking:', line)
                if line.count(":") == 2: #Split header line by two
                    packet_name, rest_of_line = line.split(":", 1)  # Split only at the first semicolon
                    f.write(f"{packet_name.strip()}:\n{rest_of_line.strip().replace("{","")}\n")
                    # print(f"\t Packet name: {packet_name.strip()}:")
                    # print(f"\tRest of the line: {rest_of_line.strip()}")
                elif "{" in line and "}" in line:
                    before_brace = line.split('{')[0].strip()  # Part before the curly brace
                    f.write(before_brace + '\n')
                    # print('\tb4 brace:', before_brace)
                    
                    inner_content = line.split('{')[1].split('}')[0]
                    elements = inner_content.split(',')
                    # print('\telements:', elements)

                    for element in elements:
                        f.write(element.strip() + '\n')
                        # print(element.strip())
                elif line.strip() == "{" or line.strip() == "}": pass
                elif "{" in line:
                    # print('AAA', line)
                    line = line.replace("{",'')
                    f.write(line + '\n')
                    # print('adding:', line)
                else:
                    f.write(line + '\n')
                
            # print(f)
            f.close()


#Put all inputs into files vector
for promptname in os.listdir(path):
    promptpath = os.path.join(path,promptname)
    # print('Prompt folder:', promptpath)

    match promptpath:
        # case 'input\\prompts1a\\chatafl':
        #     parse_text_chatafl(promptpath)
        # case 'input\\prompts1a\\rag':
        #     parse_text_rag(promptpath)
        case 'input\\prompts1a\\context':
            parse_text_context(promptpath)


# def count_packets(inputs):
#     for line in inputs:
#         line = line.split()
#         packet_header = " ".join(line[:3])
#         if '{' in packet_header:
#             packet_header = packet_header.split('{')[0] #Remove lines with '{' in it
#         packet_header = packet_header.replace(':','')

#         # print('Debugging count_packets:', packet_header)
#         #Filter out names that don't include packet in them
#         if 'packet' not in packet_header.lower(): continue
        
#         if packet_header not in packet_counters:
#             packet_counters[packet_header] = 0
#         packet_counters[packet_header] += 1
            
# #Getting packet information
# for i, vector in enumerate(files):
#     #Iterate over each line and extract packet info
#     count_packets(vector)

# #Print packet counters
# print(packet_counters)

# #Plot and save bar graphs
# output_dir = "output/evaluation"
# os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

# bars = plt.bar(packet_counters.keys(), packet_counters.values())
# plt.title("Packet Type Counts for 50 Chatgpt-4o generated inputs")
# plt.xlabel("Packet Type")
# plt.ylabel("# Occurences")
# plt.ylim(0, 55)
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()

# for bar in bars:
#     height = bar.get_height()
#     plt.annotate(f'{height}',
#                  xy=(bar.get_x() + bar.get_width() / 2, height),
#                  xytext=(0, 3),  # 3 points vertical offset
#                  textcoords="offset points",
#                  ha='center', va='bottom')

# plt.savefig(os.path.join(output_dir, "packet_type_counts.png"))
# plt.show()
