#Code to get all hex values in raw_hex_list and outputs the ground truth values for task 1b
import os
path = 'input/prompts1b/raw_hex_list'
destination_dir = 'input/prompts1b/groundtruth'
gt_files = ['input/prompts1b/groundtruth/initial', 'input/prompts1b/groundtruth/handshake', 'input/prompts1b/groundtruth/retry', 'input/prompts1b/groundtruth/versionnego', 'input/prompts1b/groundtruth/1rtt', 'input/prompts1b/groundtruth/0rtt']

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir): os.makedirs(destination_dir)

for gt_file in gt_files:
    if not os.path.exists(gt_file):
        os.makedirs(gt_file)

# Iterate through all subfolders in the root directory
for subdir, dirs, files in os.walk(path):
    # print(f'subdir:{subdir}\ndirs:{dirs}')
    for file in files:
        # print('Filename:', file)

        match file:
            case 'binary_extractor_0rtt.txt':
                # Construct the full file path
                file_path = os.path.join(subdir, file)
                
                # Open and read the contents of the file
                with open(file_path, 'r') as f:
                    first_packet = False
                    for i, line in enumerate(f):
                        if i > 50: continue
                        
                        #Remove spaces in line
                        line = line.replace(' ','')
                        temp, line = line.split(':') #Line = Get hex string, first_check = Check if first line
                        # print('Hex string: ', line)
                        
                        temp = temp.split(',')[1]

                        #Get header form, fixed bit, long packet type, reserved bits, and packet number length
                        temp = line[:2]
                        line = line[2:] #Truncate line
                        bin_str = bin(int(temp, 16))[2:].zfill(4)
                        header_form = hex(int(bin_str[0],2))
                        fixed_bit = hex(int(bin_str[1],2))
                        
                        long_packet_type = '0x' + bin_str[2:4]
                        reserved_bits = '0x' + bin_str[4:6]
                        packet_number_length = '0x' + bin_str[6:8]

                        #Get version
                        temp = line[:8]
                        line = line[8:]
                        version = '0x' + temp

                        #Get destination connection ID length (8)
                        temp = line[:2]
                        line = line[2:]
                        dest_connect_id_len = '0x' + temp

                        #Get destination connection id (0..160)
                        temp_length = int(dest_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
                        temp = line[:temp_length]
                        line = line[temp_length:]
                        dest_connect_id = '0x' + temp
                        # print(temp)

                        #Get source connection id length (8)
                        temp = line[:2]
                        line = line[2:]
                        src_connect_id_len = '0x' + temp
                        
                        #Get source connection id
                        temp_length = int(src_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
                        temp = line[:temp_length]
                        line = line[temp_length:]
                        src_connect_id = '0x' + temp

                        #Get length #Always set to 4015 need to explain < Chatgpt not good in decoding stuff. For ground truth, length is the encoded length. Do not want server to perform any decoding function to keep it simple. 
                        temp = line[:4]
                        line = line[4:]
                        length = '0x' + temp
                        # print('Length:', length)

                        #Get Packet Number. Use 4 bytes
                        temp = line[:8]
                        line = line[8:]
                        packet_number = '0x' + temp
                        # print('Packet number', packet_number)
                        #In Packet Number field, least significant two bits (those with a mask of 0x03) of byte 0 contain the length of the Packet Number field, encoded as an unsigned two-bit integer that is one less than the length of the Packet Number field in bytes. That is, the length of the Packet Number field is the value of this field plus one

                        #Remaining line for packet payload
                        packet_payload = '0x' + line

                        f = open(f"input/prompts1b/groundtruth/0rtt/{i+1}.txt", "w")
                        f.write(f'Header Form (1): {header_form}')
                        f.write(f'\nFixed Bit (1): {fixed_bit}')
                        f.write(f'\nLong Packet Type (2): {long_packet_type}')
                        f.write(f'\nReserved Bits (2): {reserved_bits}')
                        f.write(f'\nPacket Number Length (2): {packet_number_length}')
                        f.write(f'\nVersion (32): {version}')
                        f.write(f'\nDestintion Connection ID Length (8): {dest_connect_id_len}')
                        f.write(f'\nDestination Connection ID (0..160): {dest_connect_id}')
                        f.write(f'\nSource Connection ID Length (8): {src_connect_id_len}')
                        f.write(f'\nSource Connection ID (0..160): {src_connect_id}')
                        f.write(f'\nLength (i): {length}')
                        f.write(f'\nPacket Number (8..32): {packet_number}')
                        f.write(f'\nPacket Payload (8..): {packet_payload}')
                        f.close()

            # case 'binary_extractor_1rtt.txt':
            #     # Construct the full file path
            #     file_path = os.path.join(subdir, file)
                
            #     # Open and read the contents of the file
            #     with open(file_path, 'r') as f:
            #         for i, line in enumerate(f):
            #             if i > 50: continue
            #             print(line)

            #             #Remove spaces in line
            #             line = line.replace(' ','')
            #             temp, line = line.split(':') #Line = Get hex string, first_check = Check if first line
            #             # print('\nHex string: ', line)

            #             #Get header form, fixed bit, spin bit, reserverd bits, key phase, packet number length
            #             temp = line[:2]
            #             line = line[2:]
            #             bin_str = bin(int(temp, 16))[2:].zfill(8)
            #             # print(bin_str)
                        
            #             header_form = hex(int(bin_str[0],2)) #First digit
            #             fixed_bit = '0x' + bin_str[1] #2 
            #             spin_bit = '0x' + bin_str[2] #3
            #             reserved_bits = '0x' + bin_str[3:5] #4-5
            #             key_phase = '0x' + bin_str[5] #6
            #             packet_number_length = '0x' + bin_str[6:8] #7-8

            #             #Get destination connection id #NOTE length is always 16 hexadecimal digits
            #             temp = line[:16]
            #             line = line[16:]
            #             destination_connection_id = '0x' + temp
                        
            #             #Get packet number #NOTE packet is sent by client if destination connection id is below
            #             # if destination_connection_id == "1d5b0380bd0c3907" #(4 bytes. Else 1 byte)
            #             if temp == "1d5b0380bd0c3907":
            #                 hex_len = 4
            #             else:
            #                 hex_len = 2
                        
            #             temp = line[:hex_len]
            #             line = line[hex_len:]
                        
            #             packet_number = '0x' + temp

            #             #Get packet payload
            #             packet_payload = '0x' + line

            #             # print('header form: ', header_form)
            #             # print('fixed bit: ', fixed_bit)
            #             # print('spin bit: ', spin_bit)
            #             # print('reserved bits:', reserved_bits)
            #             # print('key phase:', key_phase)
            #             # print('packet num length: ', packet_number_length)
            #             # print('destination connection id: ', destination_connection_id)
            #             # print('packet number: ', packet_number)
            #             # print('packet payload: ', packet_payload)

            #             f = open(f"input/prompts1b/groundtruth/1rtt/{i+1}.txt", "w")
            #             f.write(f'Header Form (1): {header_form}')
            #             f.write(f'\nFixed Bit (1): {fixed_bit}')
            #             f.write(f'\nSpin Bit (1): {spin_bit}')
            #             f.write(f'\nReserved Bits (2): {reserved_bits}')
            #             f.write(f'\nKey Phase (1): {key_phase}')
            #             f.write(f'\nPacket Number Length (2): {packet_number_length}')
            #             f.write(f'\nDestination Connection ID (0..160): {destination_connection_id}')
            #             f.write(f'\nPacket Number (8..32): {packet_number}')
            #             f.write(f'\nPacket Payload (8..): {packet_payload}')
            #             f.close()

            # case 'binary_extractor_versionnego.txt':
            #     # Construct the full file path
            #     file_path = os.path.join(subdir, file)
                
            #     # Open and read the contents of the file
            #     with open(file_path, 'r') as f:
            #         first_packet = False
            #         for i, line in enumerate(f):
            #             if i > 50: continue

            #             # print(line)
            #             #Remove spaces in line
            #             line = line.replace(' ','')
            #             temp, line = line.split(':') #Line = Get hex string, first_check = Check if first line
            #             # print('\nHex string: ', line)

            #             #Get header form
            #             temp = line[:2]
            #             line = line[2:]
            #             bin_str = bin(int(temp, 16))[2:].zfill(4)
            #             header_form = hex(int(bin_str[0],2))

            #             #Get unused
            #             unused = '0x' + bin_str[1:]

            #             #Get version
            #             temp = line[:8]
            #             line = line[8:]
            #             version = '0x' + temp

            #             #Get destination connection ID length (8)
            #             temp = line[:2]
            #             line = line[2:]
            #             dest_connect_id_len = '0x' + temp

            #             #Get destination connection id (0..2040)
            #             temp_length = int(dest_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
            #             temp = line[:temp_length]
            #             line = line[temp_length:]
            #             dest_connect_id = '0x' + temp
            #             # print(temp)

            #             #Get source connection ID length (8)
            #             temp = line[:2]
            #             line = line[2:]
            #             src_connect_id_len = '0x' + temp

            #             #Get source connection id (0..2040)
            #             temp_length = int(src_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
            #             temp = line[:temp_length]
            #             line = line[temp_length:]
            #             src_connect_id = '0x' + temp
            #             # print(temp)

            #             #Get supported version (32)
            #             # supported_version = '0x' + line
            #             supported_version = ['0x' + line[i:i + 8].strip() for i in range(0, len(line), 8) if line[i:i + 8].strip()]

            #             # print('header form: ', header_form)
            #             # print('unused: ', unused)
            #             # print('version: ', version)
            #             # print('destination connection id length: ', dest_connect_id_len)
            #             # print('destination connection id: ', dest_connect_id)
            #             # print('source connection id length: ', src_connect_id_len)
            #             # print('source connection id: ', src_connect_id)
            #             # print('supported version: ', supported_version)

            #             f = open(f"input/prompts1b/groundtruth/versionnego/{i+1}.txt", "w")
            #             f.write(f'Header Form (1): {header_form}')
            #             f.write(f'\nUnused (7): {unused}')
            #             f.write(f'\nVersion (32): {version}')
            #             f.write(f'\nDestintion Connection ID Length (8): {dest_connect_id_len}')
            #             f.write(f'\nDestination Connection ID (0..2040): {dest_connect_id}')
            #             f.write(f'\nSource Connection ID Length (8): {src_connect_id_len}')
            #             f.write(f'\nSource Connection ID (0..2040): {src_connect_id}')
            #             f.write(f'\nSupported Version (32): {supported_version}')
            #             f.close()

            case 'binary_extractor_initial.txt':
                # Construct the full file path
                file_path = os.path.join(subdir, file)
                
                # Open and read the contents of the file
                with open(file_path, 'r') as f:
                    first_packet = False
                    for i, line in enumerate(f):
                        if i > 50: continue
                        
                        #Remove spaces in line
                        line = line.replace(' ','')
                        temp, line = line.split(':') #Line = Get hex string, first_check = Check if first line
                        # print('Hex string: ', line)
                        
                        temp = temp.split(',')[1]
                        if(temp == 'line1'): first_packet = True
                        #Get header form, fixed bit, long packet type, reserved bits, and packet number length
                        temp = line[:2]
                        line = line[2:] #Truncate line
                        bin_str = bin(int(temp, 16))[2:].zfill(4)
                        header_form = hex(int(bin_str[0],2))
                        fixed_bit = hex(int(bin_str[1],2))
                        
                        long_packet_type = '0x' + bin_str[2:4]
                        reserved_bits = '0x' + bin_str[4:6]
                        packet_number_length = '0x' + bin_str[6:8]

                        #Get version
                        temp = line[:8]
                        line = line[8:]
                        version = '0x' + temp

                        #Get destination connection ID length (8)
                        temp = line[:2]
                        line = line[2:]
                        dest_connect_id_len = '0x' + temp

                        #Get destination connection id (0..160)
                        temp_length = int(dest_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
                        temp = line[:temp_length]
                        line = line[temp_length:]
                        dest_connect_id = '0x' + temp
                        # print(temp)

                        #Get source connection id length (8)
                        temp = line[:2]
                        line = line[2:]
                        src_connect_id_len = '0x' + temp
                        
                        # bin_str = bin(int(hex_str, 16))[2:] #Convert hex to binary
                        # print(bin_str) 

                        #Get source connection id
                        temp_length = int(src_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
                        temp = line[:temp_length]
                        line = line[temp_length:]
                        src_connect_id = '0x' + temp

                        #Get token length #NOTE CURRENTLY token length will always be 0, need to explain < 
                        # if(first_packet == True): 
                        #     token = '0x00' #Set to 0 if no token is present. Initial packets sent by the server MUST be 0
                        # else: 
                        temp = line[:2]
                        line = line[2:]
                        token_length = '0x' + temp

                        #Get token #Always set to 0, need to explain < 
                        if token_length == '0x00': 
                            token = None

                        #Get length #always set to 4e6, need to explain < Chatgpt not good in decoding stuff. For ground truth, length is the encoded length. Do not want server to perform any decoding function to keep it simple. 
                        # temp = line[:4]
                        line = line[4:]
                        length = '0x' + '4e6' #Using preset value

                        #Get Packet Number. Use 4 bytes
                        temp = line[:8]
                        line = line[8:]
                        packet_number = '0x' + temp
                        #In Packet Number field, least significant two bits (those with a mask of 0x03) of byte 0 contain the length of the Packet Number field, encoded as an unsigned two-bit integer that is one less than the length of the Packet Number field in bytes. That is, the length of the Packet Number field is the value of this field plus one

                        #Remaining line for packet payload
                        packet_payload = line

                        f = open(f"input/prompts1b/groundtruth/initial/{i+1}.txt", "w")
                        f.write(f'Header Form (1): {header_form}')
                        f.write(f'\nFixed Bit (1): {fixed_bit}')
                        f.write(f'\nLong Packet Type (2): {long_packet_type}')
                        f.write(f'\nReserved Bits (2): {reserved_bits}')
                        f.write(f'\nPacket Number Length (2): {packet_number_length}')
                        f.write(f'\nVersion (32): {version}')
                        f.write(f'\nDestintion Connection ID Length (8): {dest_connect_id_len}')
                        f.write(f'\nDestination Connection ID (0..160): {dest_connect_id}')
                        f.write(f'\nSource Connection ID Length (8): {src_connect_id_len}')
                        f.write(f'\nSource Connection ID (0..160): {src_connect_id}')
                        f.write(f'\nToken Length (i): {token_length}')
                        f.write(f'\nToken (..): {token}')
                        f.write(f'\nLength (i): {length}')
                        f.write(f'\nPacket Number (8..32): {packet_number}')
                        f.write(f'\nPacket Payload (8..): {packet_payload}')
                        f.close()
            
            # case 'binary_extractor_handshake.txt':
            #     # Construct the full file path
            #     file_path = os.path.join(subdir, file)

            #     # Open and read the contents of the file
            #     with open(file_path, 'r') as f:
            #         first_packet = False
            #         for i, line in enumerate(f):
            #             if i > 50: continue
                        
            #             #Remove spaces in line
            #             line = line.replace(' ','')
            #             temp, line = line.split(':') #Line = Get hex string, first_check = Check if first line
            #             # print('Hex string: ', line)
                        
            #             temp = temp.split(',')[1]
            #             # if(temp == 'line1'): first_packet = True #NOTE If first handshake packet, then packet number is 0
                        
            #             #Get header form, fixed bit, long packet type, reserved bits, and packet number length
            #             temp = line[:2]
            #             line = line[2:] #Truncate line
            #             bin_str = bin(int(temp, 16))[2:].zfill(4)
            #             header_form = hex(int(bin_str[0],2))
            #             fixed_bit = hex(int(bin_str[1],2))
                        
            #             long_packet_type = '0x' + bin_str[2:4]
            #             reserved_bits = '0x' + bin_str[4:6]
            #             packet_number_length = '0x' + bin_str[6:8]

            #             #Get version
            #             temp = line[:8]
            #             line = line[8:]
            #             version = '0x' + temp

            #             #Get destination connection ID length (8)
            #             temp = line[:2]
            #             line = line[2:]
            #             dest_connect_id_len = '0x' + temp
            #             #Get destination connection id (0..160)
            #             temp_length = int(dest_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
            #             temp = line[:temp_length]
            #             line = line[temp_length:]
            #             dest_connect_id = '0x' + temp
            #             # print(temp)

            #             #Get source connection id length (8)
            #             temp = line[:2]
            #             line = line[2:]
            #             src_connect_id_len = '0x' + temp
                        
            #             # bin_str = bin(int(hex_str, 16))[2:] #Convert hex to binary
            #             # print(bin_str) 
                        
            #             #Get source connection id
            #             temp_length = int(src_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
            #             temp = line[:temp_length]
            #             line = line[temp_length:]
            #             src_connect_id = '0x' + temp

            #             #Get length #NOTE always set to ??, need to explain < Chatgpt not good in decoding stuff. For ground truth, length is the encoded length. Do not want server to perform any decoding function to keep it simple. 
            #             temp = line[:4]
            #             line = line[4:]
            #             length = temp
            #             # length = '0x' + '4e6' #Using preset value
            #             # print('length: ', temp)

            #             #Get Packet Number. Use 4 bytes #NO SECRETS IN GIVEN TEST CASES SO SET TO 0
            #             # temp = line[:8]
            #             # line = line[8:]
            #             temp = None
            #             packet_number = temp
                        
            #             #In Packet Number field, least significant two bits (those with a mask of 0x03) of byte 0 contain the length of the Packet Number field, encoded as an unsigned two-bit integer that is one less than the length of the Packet Number field in bytes. That is, the length of the Packet Number field is the value of this field plus one
            #             #Remaining line for packet payload
            #             packet_payload = line
            #             f = open(f"input/prompts1b/groundtruth/handshake/{i+1}.txt", "w")
            #             f.write(f'Header Form (1): {header_form}')
            #             f.write(f'\nFixed Bit (1): {fixed_bit}')
            #             f.write(f'\nLong Packet Type (2): {long_packet_type}')
            #             f.write(f'\nReserved Bits (2): {reserved_bits}')
            #             f.write(f'\nPacket Number Length (2): {packet_number_length}')
            #             f.write(f'\nVersion (32): {version}')
            #             f.write(f'\nDestintion Connection ID Length (8): {dest_connect_id_len}')
            #             f.write(f'\nDestination Connection ID (0..160): {dest_connect_id}')
            #             f.write(f'\nSource Connection ID Length (8): {src_connect_id_len}')
            #             f.write(f'\nSource Connection ID (0..160): {src_connect_id}')
            #             f.write(f'\nLength (i): {length}')
            #             f.write(f'\nPacket Number (8..32): {packet_number}')
            #             f.write(f'\nPacket Payload (8..): {packet_payload}')
            #             f.close()
            
            # case 'binary_extractor_retry.txt':
            #     # Construct the full file path
            #     file_path = os.path.join(subdir, file)
                
            #     # Open and read the contents of the file
            #     with open(file_path, 'r') as f:
            #         first_packet = False
            #         for i, line in enumerate(f):
            #             if i > 50: continue

            #             # print(line)
            #             #Remove spaces in line
            #             line = line.replace(' ','')
            #             temp, line = line.split(':') #Line = Get hex string, first_check = Check if first line
            #             # print('\nHex string: ', line)

            #             #Get header form, fixed bit, long packet type, unused
            #             temp = line[:2]
            #             line = line[2:] #Truncate line
            #             bin_str = bin(int(temp, 16))[2:].zfill(4)
            #             # print('bin str: ', bin_str)
            #             header_form = hex(int(bin_str[0],2))
            #             fixed_bit = hex(int(bin_str[1],2))
            #             long_packet_type = '0x' + bin_str[2:4]
            #             unused = '0x' + bin_str[4:]

            #             #Get version
            #             temp = line[:8]
            #             line = line[8:]
            #             version = '0x' + temp

            #             #Get destination connection ID length (8)
            #             temp = line[:2]
            #             line = line[2:]
            #             dest_connect_id_len = '0x' + temp

            #             #Get destination connection id (0..160)
            #             temp_length = int(dest_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
            #             temp = line[:temp_length]
            #             line = line[temp_length:]
            #             dest_connect_id = '0x' + temp
            #             # print(temp)

            #             #Get source connection ID length (8)
            #             temp = line[:2]
            #             line = line[2:]
            #             src_connect_id_len = '0x' + temp

            #             #Get source connection id (0..160)
            #             temp_length = int(src_connect_id_len[2:])*2 #Two hex values represent 1 byte, get byte from previous value
            #             temp = line[:temp_length]
            #             line = line[temp_length:]
            #             src_connect_id = '0x' + temp
            #             # print(temp)

            #             #Get retry token #NOTE: Length is 51
            #             temp = line[:102]
            #             line = line[102:]
            #             retry_token = '0x' + temp
                        
            #             #Get retry integrity tag
            #             retry_integrity_tag = '0x' + line

            #             # print('header form: ', header_form)
            #             # print('fixed bit: ', fixed_bit)
            #             # print('long packet type: ', long_packet_type)
            #             # print('unused: ', unused)
            #             # print('destination connection id length: ', dest_connect_id_len)
            #             # print('destination connection id: ', dest_connect_id)
            #             # print('source connection id length: ', src_connect_id_len)
            #             # print('source connection id: ', src_connect_id)
            #             # print('retry token: ', retry_token)
            #             # print('retry integrity tag: ', retry_integrity_tag)

            #             f = open(f"input/prompts1b/groundtruth/retry/{i+1}.txt", "w")
            #             f.write(f'Header Form (1): {header_form}')
            #             f.write(f'\nFixed Bit (1): {fixed_bit}')
            #             f.write(f'\nLong Packet Type (2): {long_packet_type}')
            #             f.write(f'\nUnused (4): {unused}')
            #             f.write(f'\nVersion (32): {version}')
            #             f.write(f'\nDestintion Connection ID Length (8): {dest_connect_id_len}')
            #             f.write(f'\nDestination Connection ID (0..160): {dest_connect_id}')
            #             f.write(f'\nSource Connection ID Length (8): {src_connect_id_len}')
            #             f.write(f'\nSource Connection ID (0..160): {src_connect_id}')
            #             f.write(f'\nRetry Token (..): {retry_token}')
            #             f.write(f'\nRetry Integrity Tag (128): {retry_integrity_tag}')
            #             f.close()
