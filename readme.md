Current code implementation for running LLM on ChatGPT

.env file excluded from repository

Files:
1) promptgeneration.py - Prompt generation for fuzzing and outputs results to packettest folder
2) eval1 - Reads in output of packettest and counts number of times each packet is outputted
3) eval2 - Reads in output of packettest and checks whether output matches with ground zero outputs

Batch API files:
1) batchprompts.js - List of prompts compiled as a Batch package
2) testbatch.py - Reads in above and sends Batch package to chatgpt
3) testbatchretrieval.py - Checks status of Batch package, retrieves and outputs results in output folder