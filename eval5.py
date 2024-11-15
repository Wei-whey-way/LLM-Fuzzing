#Part 2 for evaluations for prompts2
import os
import re
import ast
from collections import Counter

# eval_path = 'output\\prompts2\\eval\\context'
eval_path = 'output\\prompts2\\eval\\baseline'
# eval_path = 'output\\prompts2\\eval\\all'
# eval_path = 'output\\prompts2\\eval\\rag'
gt_path = 'input\\prompts2\\groundtruth'

expected_packets = ["Version Negotiation Packet", "Initial Packet", "0-RTT Packet", "Handshake Packet", "Retry Packet", "1-RTT Packet"]

number_inputs_gt = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
number_inputs_gpt = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}

missing_packet_list = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}
valid_list = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}
hallu_list = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}
matching_list = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}
mismatching_list = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}
order_list = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': []}

valid_count2 = 0
valid_count3 = 0
order_count = 0

#Iterate through ground truth
for filename in os.listdir(eval_path):
    # print('AAA', filename)

    with open(eval_path + '\\' + filename, 'r') as f:
        contents = f.readlines()
        # print(contents)
        gt_packets = []

        for line in contents:
            if 'Unique packet types' in line: #Get number of packet types in original bytestream
                unique_inputs = line.split(':')[1].strip()
                number_inputs_gt[unique_inputs] += 1
            
            if 'Number of unique packet types' in line: #Find out LLM enrichment
                enriched_inputs = line.split(':')[1].strip()
                number_inputs_gpt[unique_inputs].append(enriched_inputs)
                # print('Appending to number inputs gpt:', unique_inputs)
            
            if 'Valid' in line: #Check how many unique packet types generated
                valid = line.split(':')[1].strip()
                packets = ast.literal_eval(valid)

                # if(unique_inputs=='2'): print('Checking valid: ', packets, len(packets))
                
                valid_list[unique_inputs].append(len(packets))
                # if(unique_inputs=='2'): print(len(valid_list[unique_inputs]), sum(valid_list[unique_inputs]))
                    
            if 'Hallucinated' in line: #Check how many packet types hallucinated
                hallucinations = line.split(':')[1].strip()
                hallu_packets = ast.literal_eval(hallucinations)
                hallu_list[unique_inputs].append(len(hallu_packets))
                # print('Debugging: Num hallu', len(hallu_packets))
            
            if 'Order' in line:
                order = line.split(':')[1].strip()
                temp = [item.strip() for item in order.split(',')]
                order = temp
                
                #Debugging order
                # if(unique_inputs=='2'): 
                #     print(f'{order_count+1} Debugging order:', order)
                #     order_count += 1
                # if(unique_inputs=='2'): print(f'\nChecking order({unique_inputs})', order, len(order))

                if(len(order) == 1):
                    if '(Fail)' in order[0]: order_list[unique_inputs].append(0)
                    elif '(Half)' in order[0]: order_list[unique_inputs].append(0.5)
                    elif '(Pass)' in order[0]: order_list[unique_inputs].append(1)
                    
                    # if('Hallucination') not in order[0] and (unique_inputs=='2'): print(f'\tLength of order list({unique_inputs})', len(order_list[unique_inputs]), order_list[unique_inputs])
                
                else:
                    # print('Order (Length > 1):', order, len(order), f', Num hallucinations: {len(hallu_packets)}') #Average out order score if multiple
                    order_sum = 0
                    order_len = 0
                    for i in order:
                        # print('Checking length > 1', i)
                        if '(Pass)' in i:
                            order_sum += 1
                            order_len += 1
                        elif '(Half)' in i:
                            order_sum += 0.5
                            order_len += 1
                        elif '(Fail)' in i:
                            order_len += 1
                    
                    average_sum = order_sum / order_len
                    # print('\tAverage sum order: ', average_sum, f'| {order_sum}/{order_len}')
                    order_list[unique_inputs].append(average_sum)
                    # if(unique_inputs=='2') and ('Hallucination' not in i): print(f'\tLength of order list({unique_inputs})', len(order_list[unique_inputs]), order_list[unique_inputs])

#Print output
print('Number of prompts', number_inputs_gt, '\n')

print('Average number unique packet types after enrichment')
average_list = {}
for i in number_inputs_gpt: #Number of enriched inputs
    list = number_inputs_gpt[i]

    #A list of lists for that many unique packet types
    if (list):
        # print(f'{list}, Length:{len(list)}\n')
        int_list = [int(item) for item in list]

        #Combining unique list with hallucination to get total packets generated
        combined_list = [a + b for a, b in zip(int_list, hallu_list[i])]
        # print(combined_list)

        average = sum(combined_list) / len(combined_list)
        print(f' {i}: {average}')

        average_list[i] = average
        

print('\nValid generations')
for i in valid_list: #Number of hallucinations
    list = valid_list[i]

    if(list):
        print(list, len(list), sum(list))
        int_list = [int(item) for item in list]

        total = sum(int_list)
        average = sum(int_list) / len(int_list)
        rate = average / 6 * 100
        print(f' {i}: {total} (Total), {average} (Average), {rate:.2f}% (Rate)')

print('\nHallucinations')
for i in hallu_list: #Number of hallucinations
    list = hallu_list[i]

    if(list):
        print(list, len(list), sum(list))
        int_list = [int(item) for item in list]
        average = sum(int_list) / len(int_list)
        rate = average / average_list[i] * 100
        print(f' {i}: {average} (Average), {rate:.2f}% (Rate)')
    
print('\nOrder')
for i in order_list: #Order score
    list = order_list[i]

    if(list):
        # print('Valid:', valid_list[i])
        # combined_sum = [a + b for a, b in zip(valid_list[i], hallu_list[i])]
        # print(combined_sum, len(combined_sum))

        print(list, len(list))
        int_list = [int(item) for item in list]
        average = sum(int_list) / len(int_list)
        print(f' {i}: {average} (Average)')