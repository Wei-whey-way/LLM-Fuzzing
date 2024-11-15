## Current code implementation for running LLM on ChatGPT

.env file excluded from repository

Files:
1) promptgeneration.py - Prompt generation for fuzzing and outputs results to packettest folder
2) eval1 - Reads in output of packettest and counts number of times each packet is outputted
3) eval2 - Reads in output of packettest and checks whether output matches with ground zero outputs


# Creating env file
- OPENAI_API_KEY = {Insert your OpenAPI key}
- To get your OpenAPI key ... **{insert instructions here}**

# Running evaluation programs
