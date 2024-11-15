#Part 1 for evaluations for prompts2
import os
import re
from collections import Counter
import ast

# path = 'output\\prompts2\\context'
# path = 'output\\prompts2\\rag'
path = 'output\\prompts2\\baseline'
# destination_dir = 'output\\prompts2\\eval\\context'
destination_dir = 'output\\prompts2\\eval\\baseline'
# destination_dir = 'output\\prompts2\\eval\\rag'
prompt2_output_files = []

# Create the evaluation directory if it doesn't exist
if not os.path.exists(destination_dir): os.makedirs(destination_dir)

#Initialise expected values for each packet type
expected_packets = [
    "Version Negotiation Packet", "Initial Packet", "0-RTT Packet", "Handshake Packet", "Retry Packet", "1-RTT Packet"
]

# Iterate through all subfolders in the root directory and extract contents into a list of dictionarys
for subdir, dirs, files in os.walk(path):
    # print(f'subdir:{subdir}\ndirs:{dirs}\nfiles:{files}')
    if subdir == path:
        for file in files:
            filepath = os.path.join(path,file)
            id = filepath.replace(f'{path}\\output', '').replace('.txt','')
            print(f'File {id}: {file}')
            
            with open(filepath, 'r') as f: #Read each file
                #Create evaluation output file
                output_file = (f'{destination_dir}\\{file}')
                # print(output_file)
                
                lines = (f.readlines())

                f = open(output_file, "w")
                contents = {}
                generated_contents = []
                for line in lines:
                    if line.strip(): #Skip empty lines
                        # print(line)
                        if line.startswith("Line") or line.startswith("{Line"): #Find out what are the identified packets
                            #Preprocessing
                            line = line.split(':')
                            # print(line)
                            packet_name = line[1].strip()
                            line = line[0].strip('\n').replace('}','').replace('{','')
                            # print('AAAA', line)

                            #Appending to dictionary
                            if line in contents:
                                if contents[line] == packet_name: continue
                                # else: print('uhoh mismatch', line, packet_name, contents[line])
                            else:
                                contents[line] = packet_name
                            # print(line, packet_name)
                        
                        else: #Else condition for packets that arent identified in bytestream
                            # print('AAA debugging line in else condition: ', line)
                            if ('line') in line.lower(): #Further preprocessing
                                line = line.split("Line")[0].split("line")[0].strip().replace(".","")
                                # print('bbbb', line)
                            
                            #Split line
                            line = line.split(':')

                            #Skip blank values
                            if any(not item.strip() for item in line) or ('Missing packets' in line):
                                # print(f"List {line} ignored.")
                                continue
                            elif (len(line) == 1): #Debugging exceptions
                                # print(f'Length 1 exception {id} skipped:', line)
                                continue
                            else:
                                # print("List is valid:", line, len(line))
                                packet_name = line[0].strip().replace('{','').replace('}','')
                                line = line[1].strip().replace('}','').replace('{','')

                                # print(packet_name, line)
                                generated_content = [packet_name, line]
                                generated_contents.append(generated_content)

                # print(contents)
                f.write(str(contents) + '\n')

                valid_bytestream_list = []
                hallucinated_list = []

                for packet in generated_contents:
                    #Validity + Hallucination of generated packet type
                    bytestream = packet[1].replace(' ','').replace('.','').replace('{','').strip()
                    # print('AAAA, checking:', bytestream)
                    #Check if string is hexadecimal
                    if (bytestream.isalnum() and all(c in '0123456789abcdefABCDEF' for c in bytestream)):
                        # print(f'{bytestream} is valid')

                        #Check what was the packet type generated
                        version = bytestream[3:11] #Check version

                        match version:
                            case '00000000': #Check for version negotiation
                                # print('Check ver nego: ', bytestream)
                                
                                #Check if header form (1) == 1
                                header_form = bin(int(bytestream[0],16))[2:3]
                                # print('hf:', header_form)

                                if(header_form == '1'):
                                    # print(f'{bytestream} passes! Registered as version nego')
                                    valid_bytestream_list.append([f'Version negotiation', bytestream])
                                else:
                                    # print(f'{bytestream} did not pass for version nego')
                                    hallucinated_list.append(bytestream)

                            
                            case '00000001': #Check for 0-rtt, initial, retry, handshake
                                # print('Version 1: ', bytestream)
                                #Check first few parameters
                                binary = bin(int(bytestream[0],16))[2:]
                                longHeaderCheck = binary[:2]
                                packetType = binary[2:]
                                # print(longHeaderCheck, packetType)
                                
                                if (longHeaderCheck == '11'):
                                    match packetType:
                                        case '00': valid_bytestream_list.append([f'Initial Packet', bytestream])
                                        case '01': valid_bytestream_list.append([f'0-RTT Packet', bytestream])
                                        case '10': valid_bytestream_list.append([f'Handshake Packet', bytestream])
                                        case '11': valid_bytestream_list.append([f'Retry Packet', bytestream])
                                else:
                                    # print(f'{bytestream} did not pass for long header')
                                    hallucinated_list.append(bytestream)

                            case _: #Check for 1-rtt
                                # print('1-RTT ', bytestream)
                                #Check first few parameters
                                oneRttCheck = bin(int(bytestream[0],16))[2:4]
                                # print(oneRttCheck)

                                if(oneRttCheck) == '01':
                                    # print(f'{bytestream} passes! Registered as 1-rtt')
                                    valid_bytestream_list.append([f'1-RTT', bytestream])
                                else:
                                    # print(f'{bytestream} did not pass for 1-rtt')
                                    hallucinated_list.append(bytestream)
                    else:
                        # print(f'{bytestream} invalid\n')
                        hallucinated_list.append(bytestream)

                # Find all unique packet types
                with open(f'input/prompts2/groundtruth/{id}.txt','r') as gt:
                    lines = gt.readlines()

                    for line in lines:
                        if '{' in line:
                            line = ast.literal_eval(line)
                            # print(line)

                            #Get all unique packets
                            unique_packets = {key: value for key, value in line.items() if value != 0}
                            unique_packets_lower = [key.lower() for key in unique_packets]
                            # print(unique_packets_lower)
                            f.write(f"Unique packet types (GT): {len(unique_packets)}\n")      
                            
                            #Find out if valid packet types exist in ground truth packets
                            if(len(valid_bytestream_list)>0):
                                # print('Valid bytestreams: ', valid_bytestream_list)
                                for item in valid_bytestream_list:
                                    packet_name = item[0].lower().split(' (')[0]
                                    # print(packet_name)

                                    if packet_name not in unique_packets_lower:
                                        unique_packets[item[0]] = 1
                                        f.write(f"Packet types: {unique_packets.keys()}\n")
                                        f.write(f"Number of unique packet types: {len(unique_packets)}\n")                
                            else:
                                f.write(f"Packet types: {unique_packets.keys()}\n")
                                f.write(f"Number of unique packet types: {len(unique_packets)}\n")                

                #Write output 
                f.write(f'Valid: {valid_bytestream_list}\n')
                f.write(f'Hallucinated: {hallucinated_list}\n')

                f.close()
                