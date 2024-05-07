from openai import OpenAI
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 
client = OpenAI()

batch_input_file = client.files.create(
  file=open("batchprompts.jsonl", "rb"),
  purpose="batch"
)

print(batch_input_file)

batch_job = client.batches.create(
    input_file_id=batch_input_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": "nightly eval job"
    }
)

# batch_job.id = "file-ShJt2oEpQJlKTl5BTQNyrRdG"
print("Batch prompt successfully uploaded.\nBatch job: ", batch_job)
# batch_metadata = client.batches.retrieve(batch_input_file_id)

#Checking batch status
batch_job = client.batches.retrieve(batch_job.id)
print(batch_job)

#Retrieving results
result_file_id = batch_job.output_file_id
result = client.files.content(result_file_id).content
result_file_name = "output/batch_job_results.jsonl"

with open(result_file_name, 'wb') as file:
    file.write(result)