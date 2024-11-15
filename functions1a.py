import os
import re
import matplotlib.pyplot as plt
from collections import Counter
from difflib import SequenceMatcher

output_dir = "output/evaluation"

#Initialise expected values for each packet type
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
        "Destination Connection ID Length (8)": "<Value>",
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
        "Destination Connection ID Length (8)": "<Value>",
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
    },
    "1-RTT Packet": {
        "Header Form (1)": "0x0",
        "Fixed Bit (1)": "0x1",
        "Spin Bit (1)": "<Value>",
        "Reserved Bits (2)": "<Value>",
        "Key Phase (1)": "<Value>",
        "Packet Number Length (2)": "<Value>",
        "Destination Connection ID (0..160)": "<Value>",
        "Packet Number (8..32)": "<Value>",
        "Packet Payload (8..)": "<Value>",
    }
}

#Function to get accuracy of lists
def get_accuracy(packet_count, counters):
    for item in counters:
        if packet_count[item] == 0: continue
        # print('\t', len(counters[item]), counters[item])
        average = sum(counters[item])/len(counters[item])
        # print(f'\t{item}:\tAverage:', )
        
        #Get non zero items
        # filtered_list = [item for item in counters[item] if item != 0]
        # average = sum(filtered_list)/len(filtered_list)
        print(f'\t{item}: {average}')
    return

#Function to parse input text into a readable format
def parse_text(text):
    pairs = text.split(',')
    parsed_dict = {}
    for pair in pairs:
        # Trim whitespace from the beginning and end
        pair = pair.strip()
        if pair:
            # Split field and value
            field_value = pair.split(': ')
            if len(field_value) == 2:
                field = field_value[0].strip()
                value = field_value[1].strip('<> ')
                parsed_dict[field] = value
    
    return parsed_dict

#Function to format a list into a dictionary with key value pairs
def dictconversion(packet):
    packet_dict = {}
    for item in packet:
        # print('DEBUGGING DICT:', item)
        
        # Split each item at the colon (':')
        if ':' in item:
            key_value_pair = item.split(':')
            key = key_value_pair[0].strip()
            value = key_value_pair[1].strip()

            # print(f'Debugging dictconversion:\tKey {key}\twith value {value}')

            # Convert binary to hexadecimals
            try:
                if ('x' not in value) and ('<' not in value and '>' not in value):  # Stop placeholder and hexadecimals
                    binary = {'0', '1'}
                    string = set(value)

                    # If first two values in string contain 0b, remove them
                    if value[:2] == '0b':
                        value = value[2:]

                    # Convert string to an integer
                    if binary == string or string == {'0'} or string == {'1'}:
                        value = int(value, 2)  # Convert binary to integer
                    else:
                        value = int(value)  # Convert to integer

                    # Convert integer to hexadecimal
                    value = hex(value)
            
            except ValueError:
                # Handle cases where conversion fails by keeping the original value
                pass
            
            # Add the key-value pair to the dictionary
            packet_dict[key] = value
    
    return packet_dict

#Function to find out the missing rate 
def miss_hallu_count(list1, list2, type):
    count = 0
    for key in list1:
        # print('\t', key)
        if key not in list2:
            # print(f"key {key} is a {type} field\n")
            count += 1

    return count

def output_miss_hallu_seq(list, method):
    filepath = os.path.join(output_dir, 'Eval_tables.txt')
    # print(f'output_miss_hallu_seq\n{method} list:', list)

    #Calculate average miss rate for each packet type
    packet = {}
    for packet_type, rate in list:
        # print('DEBUGGING OUTPUT_MISS_HALLU:', packet_type, ': ', rate)
        if packet_type not in packet:
            packet[packet_type] = []
        packet[packet_type].append(rate)

    # print('Debugging outputmisshallu:', packet)
    # for packets in packet:
    #           #Name  #Values            #Size
    #     print(packets, packet[packets], len(packet[packets]))

    # Get total number of fields
    counts = {packet_type: len(count) for packet_type, count in packet.items()}
    
    # Multiply counts by number of field it has
    factors = {'Initial Packet': 15, '0-RTT Packet': 13, 'Handshake Packet': 13, 'Retry Packet': 11, '1-RTT Packet': 9}
    multiplied_counts = {packet_type: counts[packet_type] * factors.get(packet_type, 1) for packet_type in counts}

    # Get average number of occurrences
    for packets in packet:
        num_occurrences = sum(packet[packets]) # Total count of occurrences
        # print('length of occurence', len(packet[packets]))
        avg_occurrences = sum(packet[packets])/len(packet[packets]) # Average occurrences
        
        rate = num_occurrences/multiplied_counts[packets]
        # print(f"# {method} {packets}: {num_occurrences}\n\taverage # occurrences: {avg_occurrences}\n\trate: {rate}")

        with open(filepath, 'a') as file:
            file.write(f"{method} {packets}: Sum occurrences = {num_occurrences}\n\taverage # occurrences: {avg_occurrences}\n\trate: {rate}\n")
        
def packet_value_match(fv_pair, expected_pair, initial_count, zero_rtt_count, handshake_count, retry_count, one_rtt_count):
    #The count of above are the # of packets of that type 

    # print(f'DEBUGGING packet_value_match:\n\tKeys:{fv_pair}')#\n\tExpected keys:{expected_pair}')
    match_initial_count = 0
    match_0rtt_count = 0
    match_handshake_count = 0
    match_retry_count = 0
    match_1rtt_count = 0

    miss_initial_count = 0
    miss_0rtt_count = 0
    miss_handshake_count = 0
    miss_retry_count = 0
    miss_1rtt_count = 0
    
    fv_count_initial = []
    fv_count_0rtt = []
    fv_count_handshake = []
    fv_count_retry = []
    fv_count_1rtt = []

    fv_rate_initial = []
    fv_rate_0rtt = []
    fv_rate_handshake = []
    fv_rate_retry = [] 
    fv_rate_1rtt = []

    #Loop through each packet type in the list
    for packet_type in fv_pair.keys():
        # print('Packet type:', packet_type)
        
        #If packet exists continue
        if packet_type in expected_pair:
            fv_list = fv_pair[packet_type]
            fv_expected = expected_pair[packet_type]
            
            #Extract each field value pair from the list as a tuple
            for (tuple_1, tuple_2) in zip(fv_list, fv_expected):
                field_1, values_1 = tuple_1 #fields and values are a list
                field_2, values_2 = tuple_2

                matching_fv_count = 0

                #Debugging retry packet
                # if packet_type == 'Retry Packet':
                #     print(f"DEBUGGING Packet Value match:\nField 1 (gpt):{field_1}\n\nField 2 (expected): {field_2}\n")
                
                #Eval method 4, matching field names
                for field in field_2:
                    if field in field_1:
                        match packet_type:
                            case "Initial Packet": match_initial_count += 1
                            case "0-RTT Packet": match_0rtt_count += 1
                            case "Handshake Packet": match_handshake_count += 1
                            case "Retry Packet": match_retry_count += 1
                            case "1-RTT Packet": match_1rtt_count += 1
                            case _:
                                print(f'PACKET_VALUE_MATCH: {field} not in expected fields')
                                continue
                    else:
                        match packet_type:
                            case "Initial Packet": miss_initial_count += 1
                            case "0-RTT Packet": miss_0rtt_count += 1
                            case "Handshake Packet": miss_handshake_count += 1
                            case "Retry Packet": miss_retry_count += 1
                            case "1-RTT Packet": miss_1rtt_count += 1
                            case _:
                                print(f'PACKET_VALUE_MATCH: {field} not in expected fields')
                                continue

                # Output the results
                # print(f"{packet_type} - Tuple {i+1}:")
                # print(f"  Matching Fields: {matching_field_count}/{len(field_1)}")
                
                #Eval method 4.2, matching field-value pair
                # Iterate through each key-value pair in tuple_1
                for key, value in zip(field_1, values_1):
                    if key in field_2:
                        # Find the index of the matching key in tuple_2
                        index_in_tuple_2 = list(field_2).index(key)
                        value_2 = list(values_2)[index_in_tuple_2]
                        
                        # Check if the values match
                        if value == value_2:
                            matching_fv_count += 1
                        # else: print(f"Value: {value} incorrect match with {value_2}")
                
                total_pairs = len(field_1)
                # print(f"{packet_type}: {matching_fv_count} out of {total_pairs} key-value pairs match.")
                match packet_type:
                    # case "Version Negotiation Packet": fv_count_version.append(len(keys))
                    case "Initial Packet": 
                        fv_count_initial.append(matching_fv_count)
                        fv_rate_initial.append(matching_fv_count/total_pairs)
                    case "0-RTT Packet": 
                        fv_count_0rtt.append(matching_fv_count)
                        fv_rate_0rtt.append(matching_fv_count/total_pairs)
                    case "Handshake Packet": 
                        fv_count_handshake.append(matching_fv_count)
                        fv_rate_handshake.append(matching_fv_count/total_pairs)
                    case "Retry Packet": 
                        fv_count_retry.append(matching_fv_count)
                        fv_rate_retry.append(matching_fv_count/total_pairs)
                    case "1-RTT Packet": 
                        fv_count_1rtt.append(matching_fv_count)
                        fv_rate_1rtt.append(matching_fv_count/total_pairs)
                    case _:
                        print(f'PACKET_VALUE_MATCH: {key} not in expected fields')
                        continue
        else:
            print(f"DEBUGGING packet_value_match: {packet_type} is not present in packet_data_2")
    
    #Output results
    # print(f'Matching fields\nInitial packet:\n\tAverage occurrences: {match_initial_count/initial_count}\n\tRate: {match_initial_count/(match_initial_count+miss_initial_count)}')
    # print(f'0-RTT packet\n\tAverage occurrences: {match_0rtt_count/zero_rtt_count}\n\tRate: {match_0rtt_count/(match_0rtt_count+miss_0rtt_count)}')
    # print(f'Handshake packet\n\tAverage occurrences: {match_handshake_count/handshake_count}\n\tRate: {match_handshake_count/(match_handshake_count+miss_handshake_count)}')
    # print(f'Retry packet\n\tAverage occurrences: {match_retry_count/retry_count}\n\tRate: {match_retry_count/(match_retry_count+miss_retry_count)}')
    # print(f'\tmatch_retry_count: {match_retry_count}\n\tmiss_retry_count:{miss_retry_count}\n\tretry_count:{retry_count}\n')

    # print(f'Initial packet:\n\tAverage occurrences: {sum(fv_count_initial)/len(fv_count_initial)}\n\tRate: {sum(fv_rate_initial)/len(fv_rate_initial)}')
    # print(f'0-RTT packet:\n\tAverage occurrences: {sum(fv_count_0rtt)/len(fv_count_0rtt)}\n\tRate: {sum(fv_rate_0rtt)/len(fv_rate_0rtt)}')
    # print(f'Handshake packet:\n\tAverage occurrences: {sum(fv_count_handshake)/len(fv_count_handshake)}\n\tRate: {sum(fv_rate_handshake)/len(fv_rate_handshake)}')
    # print(f'Retry packet:\n\tAverage occurrences: {sum(fv_count_retry)/len(fv_count_retry)}\n\tRate: {sum(fv_rate_retry)/len(fv_rate_retry)}')
    
    filepath = os.path.join(output_dir, 'Eval_tables_Matching.txt')
    with open(filepath, 'a') as file:
        #Matching fields
        file.write(f'Matching fields\nInitial packet:\n\tAverage occurrences: {match_initial_count/initial_count}\n\tRate: {match_initial_count/(match_initial_count+miss_initial_count)}\n')
        file.write(f'0-RTT packet\n\tAverage occurrences: {match_0rtt_count/zero_rtt_count}\n\tRate: {match_0rtt_count/(match_0rtt_count+miss_0rtt_count)}\n')
        file.write(f'Handshake packet\n\tAverage occurrences: {match_handshake_count/handshake_count}\n\tRate: {match_handshake_count/(match_handshake_count+miss_handshake_count)}\n')
        file.write(f'Retry packet\n\tAverage occurrences: {match_retry_count/retry_count}\n\tRate: {match_retry_count/(match_retry_count+miss_retry_count)}\n')
        file.write(f'1-RTT packet\n\tAverage occurrences: {match_1rtt_count/one_rtt_count}\n\tRate: {match_1rtt_count/(match_1rtt_count+miss_1rtt_count)}\n')

        #Matching field value pairs
        file.write(f'Matching Field Value pairs\nInitial packet:\n\tAverage occurrences: {sum(fv_count_initial)/len(fv_count_initial)}\n\tRate: {sum(fv_rate_initial)/len(fv_rate_initial)}\n')
        file.write(f'0-RTT packet:\n\tAverage occurrences: {sum(fv_count_0rtt)/len(fv_count_0rtt)}\n\tRate: {sum(fv_rate_0rtt)/len(fv_rate_0rtt)}\n')
        file.write(f'Handshake packet:\n\tAverage occurrences: {sum(fv_count_handshake)/len(fv_count_handshake)}\n\tRate: {sum(fv_rate_handshake)/len(fv_rate_handshake)}\n')
        file.write(f'Retry packet:\n\tAverage occurrences: {sum(fv_count_retry)/len(fv_count_retry)}\n\tRate: {sum(fv_rate_retry)/len(fv_rate_retry)}\n')
        file.write(f'1-RTT packet:\n\tAverage occurrences: {sum(fv_count_1rtt)/len(fv_count_1rtt)}\n\tRate: {sum(fv_rate_1rtt)/len(fv_rate_1rtt)}\n')

def tuple_conversion(dictionary):
    result_list = []
    #Converting the key values list into a tuple (gpt output)
    # Iterate through each key-value pair in the dictionary
    for kv in dictionary:
        keys, values = kv  # Unpack the tuple into keys and values
        # Convert keys and values to lists if they are not already
        keys_list = list(keys)
        # values_list = list(values)
        
        # Combine keys and values into a list of tuples
        # kv_pairs = list(zip(keys_list, values_list))
        result_list.append(keys_list)
        # print(kv_pairs)

    # print('Tuple_conversion: Returning: \n\t', result_list)
    return result_list

def packet_value_seq(fv_pair, expected_pair, initial_count, zero_rtt_count, handshake_count, retry_count, one_rtt_count):
    #The count of above are the # of packets of that type 
    gpt_initial = []
    gpt_0rtt = []
    gpt_handshake = []
    gpt_retry = []
    gpt_1rtt = []

    expected_initial = []
    expected_0rtt = []
    expected_handshake = []
    expected_retry = []
    expected_1rtt = []

    count_initial_list = []
    count_0rtt_list = []
    count_handshake_list = []
    count_retry_list = []
    count_1rtt_list = []

    for packet_type, dictionary in fv_pair.items():
        match packet_type:
            case 'Initial Packet': gpt_initial = tuple_conversion(dictionary)
            case '0-RTT Packet': gpt_0rtt = tuple_conversion(dictionary)
            case 'Handshake Packet': gpt_handshake = tuple_conversion(dictionary)
            case 'Retry Packet': gpt_retry = tuple_conversion(dictionary)
            case '1-RTT Packet': gpt_1rtt = tuple_conversion(dictionary)
    
    for packet_type, dictionary in expected_pair.items():
        match packet_type:
            case 'Initial Packet': expected_initial = tuple_conversion(dictionary)
            case '0-RTT Packet': expected_0rtt = tuple_conversion(dictionary)
            case 'Handshake Packet': expected_handshake = tuple_conversion(dictionary)
            case 'Retry Packet': expected_retry = tuple_conversion(dictionary)
            case '1-RTT Packet': expected_1rtt = tuple_conversion(dictionary)

    #Get sequence count
    for i, kv_tuples in enumerate(expected_initial): #Initial packet
        # print(f'Input #{i}')
        counter = 0
        for j, tuple in enumerate(kv_tuples):
            if j < len(gpt_initial[i]): #Check for boundary cases
                # print(f'{tuple} matching with {gpt_initial[i][j]}') 
                if tuple == gpt_initial[i][j]:
                    counter += 1
                # else: print(f'{tuple} did not match {gpt_initial[i][j]}') 
        count_initial_list.append(counter)
    for i, kv_tuples in enumerate(expected_0rtt): #0rtt packet
        counter = 0
        for j, tuple in enumerate(kv_tuples):
            if j < len(gpt_0rtt[i]):
                if tuple == gpt_0rtt[i][j]:
                    counter += 1
        count_0rtt_list.append(counter)
    for i, kv_tuples in enumerate(expected_handshake): #Handshake packet
        counter = 0
        for j, tuple in enumerate(kv_tuples):
            if j < len(gpt_handshake[i]):
                if tuple == gpt_handshake[i][j]:
                    counter += 1
        count_handshake_list.append(counter)
    for i, kv_tuples in enumerate(expected_retry): #Retry packet
        counter = 0
        for j, tuple in enumerate(kv_tuples):
            if j < len(gpt_retry[i]):
                if tuple == gpt_retry[i][j]:
                    counter += 1
        count_retry_list.append(counter)
    for i, kv_tuples in enumerate(expected_1rtt): #1-RTT packet
        counter = 0
        for j, tuple in enumerate(kv_tuples):
            if j < len(gpt_1rtt[i]):
                if tuple == gpt_1rtt[i][j]:
                    counter += 1
        count_1rtt_list.append(counter)

    #Output results
    # print('Debugging seq: \n\tcount_intial:', count_initial_list)
    total_fields_initial = initial_count * 15
    total_fields_0rtt = zero_rtt_count * 13
    total_fields_handshake = handshake_count * 13
    total_fields_retry = retry_count * 11
    total_fields_1rtt = one_rtt_count * 9
    
    # print(f'Initial packet:\n\tAverage occurrences: {sum(count_initial_list)/len(count_initial_list)}\n\tRate: {sum(count_initial_list)/total_fields_initial}')
    # print(f'0-RTT packet:\n\tAverage occurrences: {sum(count_0rtt_list)/len(count_0rtt_list)}\n\tRate: {sum(count_0rtt_list)/total_fields_0rtt}')
    # print(f'Handshake packet:\n\tAverage occurrences: {sum(count_handshake_list)/len(count_handshake_list)}\n\tRate: {sum(count_handshake_list)/total_fields_handshake}')
    # print(f'Retry packet:\n\tAverage occurrences: {sum(count_retry_list)/len(count_retry_list)}\n\tRate: {sum(count_retry_list)/total_fields_retry}')   

    filepath = os.path.join(output_dir, 'Eval_tables_Matching.txt')
    with open(filepath, 'a') as file:
        file.write(f'Sequence matching\nInitial packet:\n\tAverage occurrences: {sum(count_initial_list)/len(count_initial_list)}\n\tRate: {sum(count_initial_list)/total_fields_initial}\n')
        file.write(f'0-RTT packet:\n\tAverage occurrences: {sum(count_0rtt_list)/len(count_0rtt_list)}\n\tRate: {sum(count_0rtt_list)/total_fields_0rtt}\n')
        file.write(f'Handshake packet:\n\tAverage occurrences: {sum(count_handshake_list)/len(count_handshake_list)}\n\tRate: {sum(count_handshake_list)/total_fields_handshake}\n')
        file.write(f'Retry packet:\n\tAverage occurrences: {sum(count_retry_list)/len(count_retry_list)}\n\tRate: {sum(count_retry_list)/total_fields_retry}\n')  
        file.write(f'1-RTT packet:\n\tAverage occurrences: {sum(count_1rtt_list)/len(count_1rtt_list)}\n\tRate: {sum(count_1rtt_list)/total_fields_1rtt}\n')   


#Creating a horizontal bar plot
def plot_overview_graph(data, title, filename):
    # Extract keys and values
    labels = list(data.keys())
    values = list(data.values())

    # Create a horizontal bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.barh(labels, values)
    plt.xlabel('# occurences')
    
    if values:
        max_count = max(values)
    else:
        max_count = 0
    
    plt.xlim(0, max_count+5)
    plt.title(title)
    plt.tight_layout() 

    for bar in bars:
        width = bar.get_width()
        plt.annotate(f'{width}',
                     xy=(width, bar.get_y() + bar.get_height() / 2),
                     xytext=(3, 0),  # 3 points horizontal offset
                     textcoords="offset points",
                     ha='left', va='center')
        
    plt.savefig(os.path.join(output_dir, filename))