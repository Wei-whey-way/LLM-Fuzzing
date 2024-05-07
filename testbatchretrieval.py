from openai import OpenAI
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 
client = OpenAI()

#Put current batch_job_id here. Manual insertion from testbatch.py:
batch_job_id = "batch_ru5XNzr2hcihUrToyrJgDtev"

#Checking batch status
batch_job = client.batches.retrieve(batch_job_id)
print("Batch job statuses: ", batch_job)

#Retrieving results
# result_file_id = batch_job.output_file_id
# result = client.files.content(result_file_id).content
# result_file_name = "output/batch_job_results.jsonl"

# with open(result_file_name, 'wb') as file:
#     file.write(result)