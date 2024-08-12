#File to extract packet types from task_3_training_data folder
import os

# Define the source and destination directories
path = 'input/task_3_training_data'
destination_dir = 'input/prompts1b'

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Iterate through all subfolders in the root directory
for subdir, dirs, files in os.walk(path):
    for file in files:
        # print('Filename:', file)
        if file == 'seperated_encrypted.txt':
            # Construct the full file path
            file_path = os.path.join(subdir, file)
            
            # Open and read the contents of the file
            with open(file_path, 'r') as f:
                # content = f.read()
                for line in f:
                    #Remove spaces in line
                    line = line.replace(' ','')
                    
                    #Convert line from hexadecimal to binary
                    binary = bin(int(line, 16))[2:]
                    #Extract necessary packet types from the binary string
                    #Version negotiation packet <- NEED HELP. ALSO CHECK HOW MUCH YOU CAN TRUNCATE
                    #1-RTT PACKET?!?!?

                    #Format for extract packets
                    # print(binary[:5])
                                #1st      #2nd             #3-4
                    # print(binary[0], ' ', binary[1], ' ', binary[2:4])

                    #Initial packet
                    if (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '00'):
                        # print('Initial packet')
                        output_file_path = os.path.join(destination_dir, 'binary_extractor_initial.txt')
                        with open(output_file_path, 'a') as output_file:
                            output_file.write(binary + '\n')
                        # print(f"Extracted binary to {output_file_path}")
                    
                    #0-Rtt
                    elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '01'):
                        output_file_path = os.path.join(destination_dir, 'binary_extractor_0rtt.txt')
                        with open(output_file_path, 'a') as output_file:
                            output_file.write(binary + '\n')
                    
                    #Handshake
                    elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '10'):
                        output_file_path = os.path.join(destination_dir, 'binary_extractor_handshake.txt')
                        with open(output_file_path, 'a') as output_file:
                            output_file.write(binary + '\n')
                    
                    #Retry
                    elif (binary[0]=='1' and binary[1]=='1' and binary[2:4] == '11'):
                        output_file_path = os.path.join(destination_dir, 'binary_extractor_retry.txt')
                        with open(output_file_path, 'a') as output_file:
                            output_file.write(binary + '\n')
                        
                    