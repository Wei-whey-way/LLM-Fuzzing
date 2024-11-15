#File to extract packet types from task_3_training_data folder
import os

# Define the source and destination directories
path = 'input/task_3_training_data'
path2 = 'input/task_3_training_data_retry'
destination_dir = 'input/prompts1b/raw_hex_list'

# Clear the contents of previous extracted prompts but keep the files
file_paths = [
    'input/prompts1b/binary_extractor_initial.txt',
    'input/prompts1b/binary_extractor_0rtt.txt',
    'input/prompts1b/binary_extractor_retry.txt',
    'input/prompts1b/binary_extractor_handshake.txt',
    'input/prompts1b/binary_extractor_versionnego.txt'
]

for file_path in file_paths:
    if os.path.exists(file_path):
        # Open the file in write mode to clear its contents
        with open(file_path, 'w') as file:
            pass  # This effectively clears the file
# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

#Function to put in hex lines into raw_hex_list folder
def extract_raw_hex_list(packet_name, line, destination_dir):
    # print(packet_name, 'going to', destination_dir)
    
    # print(f'Now putting to {packet_name}: ', line)
    output_file_path = os.path.join(destination_dir, f'binary_extractor_{packet_name}.txt')
    
     # Check if the file exists and count the number of lines
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r') as output_file:
            line_count = sum(1 for _ in output_file)
            
        # If the file has 50 or more lines, end the program
        if line_count >= 50:
            # print(f"{packet_name} already has 50 or more lines. Ending the program.")
            return

    with open(output_file_path, 'a') as output_file: 
        output_file.write(subdir + ', line ' + str(i+1) + ': ' + line)
    
    return

# Iterate through all subfolders in the root directory
for subdir, dirs, files in os.walk(path):
    # print(f'subdir:{subdir}\tdirs:{dirs}')
    for file in files:
        # print('Filename:', file)
        if file == 'seperated_encrypted.txt':
            # Construct the full file path
            file_path = os.path.join(subdir, file)
            
            # Open and read the contents of the file
            with open(file_path, 'r') as f:
                # content = f.read()
                
                handshake_flag = False #Flag for 1-RTT Packet
                for i, line in enumerate(f):
                    #Remove spaces in line
                    line = line.replace(' ','')
                    
                    # print('Now converting: ', line)

                    binary = line[:1] #Get first characters in hex
                    binary = bin(int(binary, 16))[2:].zfill(4) #zfill to make sure that leading 0s are kept
                    # print('Binary: ', binary)
                    #Extract necessary packet types from the binary string
                    
                    #Version negotiation packet included in task1b_extractor_nego

                    #Format for extract packets
                                #1st      #2nd             #3-4
                    # print(binary[0], ' ', binary[1], ' ', binary[2:4])

                    #Initial packet
                    if (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '00'):
                        extract_raw_hex_list('initial', line, destination_dir)
                    
                    #0-Rtt
                    elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '01'):
                        extract_raw_hex_list('0rtt', line, destination_dir)

                    #Handshake
                    elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '10'):
                        extract_raw_hex_list('handshake', line, destination_dir)
                        handshake_flag = True
                        
                    #Retry included in loop below
                    
                    #1-RTT
                    if(handshake_flag == True and binary[0]=='0' and binary[1]=='1'):
                        # print('1rtt: ', line)
                        extract_raw_hex_list('1rtt', line, destination_dir)

                    # else: print('not included: ', line)

#Repeat for second folder (retry)                        
for subdir, dirs, files in os.walk(path2):
    # print(f'subdir:{subdir}\ndirs:{dirs}')
    for file in files:
        # print('Filename:', file)
        if file == 'seperated_encrypted.txt':
            # Construct the full file path
            file_path = os.path.join(subdir, file)
            
            # Open and read the contents of the file
            with open(file_path, 'r') as f:
                # content = f.read()
                for i, line in enumerate(f):
                    #Remove spaces in line
                    line = line.replace(' ','')
                    
                    # print(f'{i}: Now converting: {line}')

                    binary = line[:1] #Get first characters in hex
                    binary = bin(int(binary, 16))[2:].zfill(4) #zfill to make sure that leading 0s are kept
                    # print('Binary: ', binary)
                    #Extract necessary packet types from the binary string

                    #Format for extract packets
                                #1st      #2nd             #3-4
                    # print(binary[0], ' ', binary[1], ' ', binary[2:4])
                        
                    #Retry
                    if (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '11'):
                        # print('line', line)
                        extract_raw_hex_list('retry', line, destination_dir)
                    
                    # else: print('not included: ', line)
             