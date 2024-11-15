#File to extract packet types from task_3_training_data folder
import os

# Define the source and destination directories
path = 'input/task_1_training_data_0rtt'
destination_dir = 'input/prompts1b/raw_hex_list'

# Clear the contents of previous extracted prompts but keep the files
file_paths = [
    'input/prompts1b/binary_extractor_initial.txt',
    'input/prompts1b/binary_extractor_0rtt.txt',
    'input/prompts1b/binary_extractor_retry.txt',
    'input/prompts1b/binary_extractor_handshake.txt'
]

for file_path in file_paths:
    if os.path.exists(file_path):
        # Open the file in write mode to clear its contents
        with open(file_path, 'w') as file:
            pass  # This effectively clears the file

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir): os.makedirs(destination_dir)

#Function to put in hex lines into raw_hex_list folder
def extract_raw_hex_list(packet_name, line, destination_dir):
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
    # print(f'subdir:{subdir}\ndirs:{dirs}')
    for file in files:
        # print('Filename:', file)
        if file == 'seperated_encrypted.txt': #Use raw encrypted for negotiation folder
            # Construct the full file path
            file_path = os.path.join(subdir, file)
            
            # Open and read the contents of the file
            with open(file_path, 'r') as f:
                # content = f.read()
                for i, line in enumerate(f):
                    #Remove spaces in line
                    line = line.replace(' ','')
                    
                    # print('Now converting: ', line)
                    
                    #Check for version negotiation #NOTE Version is set to 0x0
                    version_check = line[2:10]
                    # print('version check: ', version_check)
                    if str(version_check) == "00000000":
                        extract_raw_hex_list('versionnego', line, destination_dir)

                    else:
                        binary = line[:1] #Get first characters in hex
                        binary = bin(int(binary, 16))[2:].zfill(4) #zfill to make sure that leading 0s are kept
                        # print('Binary: ', binary)
                        #Extract necessary packet types from the binary string
                        #Version negotiation packet <- NEED HELP. ALSO CHECK HOW MUCH YOU CAN TRUNCATE
                        #1-RTT PACKET?!?!?

                        #Format for extract packets
                                    #1st      #2nd             #3-4
                        # print(binary[0], ' ', binary[1], ' ', binary[2:4])

                        #0-Rtt
                        if (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '01'):
                            # print('Checking 0-rtt: ', line)
                            extract_raw_hex_list('0rtt', line, destination_dir)
                        
                        # else: print('not included: ', line)
                        
                    