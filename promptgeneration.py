from openai import OpenAI
from dotenv import load_dotenv, dotenv_values 
import os

load_dotenv() 

#Make output folder
if not os.path.exists('output'):
    os.makedirs('output')

if not os.path.exists('output/packettest'):
    os.makedirs('output/packettest')

client = OpenAI()

print("Now generating packets...")

for i in range(1, 11):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system", "content": "For the RFC9000 QUIC protocol, please provide all of the packet grammar specified in the document. You can find the document here - https://www.rfc-editor.org/rfc/rfc9000.html\n\nDesired Format:\nShot-1:\nFor the QUIC protocol, the Retry Packet client request format is below. See RFC9000 for set bytes.\nRetry Packet: {Header Form (1): <Value>\\r\\n, Fixed Bit (1): <Value>\\r\\n, Long Packet Type (2): <Value>\\r\\n, Unused (4): <Value>\\r\\n, Version (32): <Value>\\r\\n, Destination Connection ID Length (8): <Value>\\r\\n, Destination Connection ID (0..160): <Value>\\r\\n, Source Connection ID Length (8): <Value>\\r\\n, Source Connection ID (0..160): <Value>\\r\\n, Retry Token (..): <Value>\\r\\n, Retry Integrity Tag (128) <Value>\\r\\n}\n\nShot-2:\n0-RTT Packet: {Header Form (1): <Value>\\r\\n, Fixed Bit (1): <Value>\\r\\n, Long Packet Type (2): <Value>\\r\\n, Reserved Bits (2): <Value>\\r\\n, Packet Number Length (2): <Value>\\r\\n, Version (32): <Value>\\r\\n, Destination Connection ID Length (8): <Value>\\r\\n, Destination Connection ID (0..160): <Value>\\r\\n, Source Connection ID Length (8): <Value>\\r\\n, Source Connection ID (0..160): <Value>\\r\\n, Length (i): <Value>\\r\\n, Packet Number (8..32): <Value>\\r\\n, Packet Payload (8..): <Value>\\r\\n,}\n\nPlease provide all of the Long Header Packets in the desired format according to RFC9000 documentation. Display the packets line by line. For header form, fixed bit, long packet type, fill in the <Value> field to a value that is suitable based on the document that I linked above. <Value> format in hexadecimal. If the <Value> depends on the information during transmission, just remain <Value>.\n\nProvide output in this format:\n[Packet name]: {Packet content 1, content 2}"
      }
      # {
        # "role": "system", "content": "For the RFC9000 QUIC protocol, please provide all of the packet grammar specified in the document. You can find the document here - https://www.rfc-editor.org/rfc/rfc9000.html\n\nDesired Format:\nShot-1:\nFor the QUIC protocol, the Retry Packet client request format is below. See RFC9000 for set bytes.\nRetry Packet: {Header Form (1): <Value>\\r\\n, Fixed Bit (1): <Value>\\r\\n, Long Packet Type (2): <Value>\\r\\n, Unused (4): <Value>\\r\\n, Version (32): <Value>\\r\\n, Destination Connection ID Length (8): <Value>\\r\\n, Destination Connection ID (0..160): <Value>\\r\\n, Source Connection ID Length (8): <Value>\\r\\n, Source Connection ID (0..160): <Value>\\r\\n, Retry Token (..): <Value>\\r\\n, Retry Integrity Tag (128) <Value>\\r\\n}\n\nShot-2:\n0-RTT Packet: {Header Form (1): <Value>\\r\\n, Fixed Bit (1): <Value>\\r\\n, Long Packet Type (2): <Value>\\r\\n, Reserved Bits (2): <Value>\\r\\n, Packet Number Length (2): <Value>\\r\\n, Version (32): <Value>\\r\\n, Destination Connection ID Length (8): <Value>\\r\\n, Destination Connection ID (0..160): <Value>\\r\\n, Source Connection ID Length (8): <Value>\\r\\n, Source Connection ID (0..160): <Value>\\r\\n, Length (i): <Value>\\r\\n, Packet Number (8..32): <Value>\\r\\n, Packet Payload (8..): <Value>\\r\\n,}\n\nPlease provide all of the Long Header Packets in the desired format according to RFC9000 documentation. Display the packets line by line. For header form, fixed bit, long packet type, fill in the <Value> field to a value in hex that is suitable based on the document that I linked above. If the <Value> depends on the information during transmission, just remain <Value>."
      # }
    ],
    temperature=0.5,
    max_tokens=1600,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  #Extract output
  output = str(completion.choices[0].message.content)
  # print(output)
  file_path = os.path.join('output/packettest', f'output{i}.txt')
  with open(file_path, 'w') as f:
      f.write(output)

print("Testing complete")
