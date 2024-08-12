import os
import re
import matplotlib.pyplot as plt
from collections import Counter
from difflib import SequenceMatcher

output_dir = "output/evaluation"

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

            #Convert binary values to hexadecimal
            # print('DEBUGGING dictconversions value:', value, type(value))
            if ('x' not in value) and (value != '<Value>'):
                binary = {'0', '1'}
                string = set(value)

                #Convert string to an integer
                if binary == string or string == {'0'} or string == {'1'}:
                    #Convert binary to integer
                    value = int(value, 2)
                else:
                    value = int(value)
                
                #Convert integer to hexadecimal
                value = hex(value)
                    
            # Add the key-value pair to the dictionary
            packet_dict[key] = value
        else:
            # print('Debugging dictconversion, no semicolons')
            continue
    
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
    factors = {'Initial Packet': 15, '0-RTT Packet': 13, 'Handshake Packet': 13, 'Retry Packet': 11}
    multiplied_counts = {packet_type: counts[packet_type] * factors.get(packet_type, 1) for packet_type in counts}

    # Get average number of occurrences
    for packets in packet:
        num_occurrences = sum(packet[packets]) # Total count of occurrences
        print('length of occurence', len(packet[packets]))
        avg_occurrences = sum(packet[packets])/len(packet[packets]) # Average occurrences
        
        rate = num_occurrences/multiplied_counts[packets]
        print(f"# {method} {packets}: {num_occurrences}\n\taverage # occurrences: {avg_occurrences}\n\trate: {rate}")

        with open(filepath, 'a') as file:
            file.write(f"{method} {packets}: Sum occurrences = {num_occurrences}\n\taverage # occurrences: {avg_occurrences}\n\trate: {rate}\n")
        
def packet_value_match(fv_pair, expected_pair, initial_count, zero_rtt_count, handshake_count, retry_count):
    #The count of above are the # of packets of that type 

    # print(f'DEBUGGING packet_value_match:\n\tKeys:{fv_pair}\n\tExpected keys:{expected_pair}')
    match_initial_count = 0
    match_0rtt_count = 0
    match_handshake_count = 0
    match_retry_count = 0
    miss_initial_count = 0
    miss_0rtt_count = 0
    miss_handshake_count = 0
    miss_retry_count = 0
    
    fv_count_initial = []
    fv_count_0rtt = []
    fv_count_handshake = []
    fv_count_retry = []

    fv_rate_initial = []
    fv_rate_0rtt = []
    fv_rate_handshake = []
    fv_rate_retry = [] 

    for packet_type in fv_pair.keys():
        # print('Packet type:', packet_type)
        
        if packet_type in expected_pair:
            fv_list = fv_pair[packet_type]
            fv_expected = expected_pair[packet_type]
            
            for (tuple_1, tuple_2) in zip(fv_list, fv_expected):
                field_1, values_1 = tuple_1 #fields and values are a list
                field_2, values_2 = tuple_2

                matching_fv_count = 0
                
                #Check if keys match
                for field in field_1:
                    if field in field_2:
                        match packet_type:
                            case "Initial Packet": match_initial_count += 1
                            case "0-RTT Packet": match_0rtt_count += 1
                            case "Handshake Packet": match_handshake_count += 1
                            case "Retry Packet": match_retry_count += 1
                            case _:
                                print(f'PACKET_VALUE_MATCH: {field} not in expected fields')
                                continue
                    else:
                        match packet_type:
                            case "Initial Packet": miss_initial_count += 1
                            case "0-RTT Packet": miss_0rtt_count += 1
                            case "Handshake Packet": miss_handshake_count += 1
                            case "Retry Packet": miss_retry_count += 1
                            case _:
                                print(f'PACKET_VALUE_MATCH: {field} not in expected fields')
                                continue

                # Output the results
                # print(f"{packet_type} - Tuple {i+1}:")
                # print(f"  Matching Fields: {matching_field_count}/{len(field_1)}")
                
                # Iterate through each key-value pair in tuple_1
                for key, value in zip(field_1, values_1):
                    if key in field_2:
                        # Find the index of the matching key in tuple_2
                        index_in_tuple_2 = list(field_2).index(key)
                        value_2 = list(values_2)[index_in_tuple_2]
                        
                        # Check if the values match
                        if value == value_2:
                            matching_fv_count += 1
                        # else:
                        #     print(f"Value: {value} incorrect match with {value_2}")
                
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

        #Matchine field value pairs
        file.write(f'Matching Field Value pairs\nInitial packet:\n\tAverage occurrences: {sum(fv_count_initial)/len(fv_count_initial)}\n\tRate: {sum(fv_rate_initial)/len(fv_rate_initial)}\n')
        file.write(f'0-RTT packet:\n\tAverage occurrences: {sum(fv_count_0rtt)/len(fv_count_0rtt)}\n\tRate: {sum(fv_rate_0rtt)/len(fv_rate_0rtt)}\n')
        file.write(f'Handshake packet:\n\tAverage occurrences: {sum(fv_count_handshake)/len(fv_count_handshake)}\n\tRate: {sum(fv_rate_handshake)/len(fv_rate_handshake)}\n')
        file.write(f'Retry packet:\n\tAverage occurrences: {sum(fv_count_retry)/len(fv_count_retry)}\n\tRate: {sum(fv_rate_retry)/len(fv_rate_retry)}\n')
    
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