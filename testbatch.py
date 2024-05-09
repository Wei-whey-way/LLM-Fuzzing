from openai import OpenAI
from dotenv import load_dotenv

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
      "description": "3.5 batchprompts test"
    }
)

print("\nBatch prompt successfully uploaded.")