from openai import OpenAI
from dotenv import load_dotenv, dotenv_values 
import os

load_dotenv() 

#Make output folder
if not os.path.exists('output/packetadd'):
    os.makedirs('output/packetadd')

client = OpenAI()

def generate_follow_up_prompt(contents):
    # bytestream = "cd000000010822a02413909f457608a3507dc3a212c5e60044e6a1fb17a3345cb4dc64da9a54d609a48933acd97ad4e3d9277d2292a907e53e1e33010ce9a39ed9ea733405196b78636e2e11f4516c36650bd1df97a14bb5f48b38f8838e850cac39bd383ff2564179af88a6a2f762e6e41ec9c5f0b42d2f1395fa6680085a129baac26008aa61a5d6ea269cc0b7a8b101afaed95e7e7c2e1b24c6adce5fe843fda372b2c989f7d395d54ecfbd0e4eae9fcb8cd46ec76a954a6cefd6a122cdf10258510781f2bc47d4c777108d6ad75b1a55157d809a40a57d6bd777e305bd290fc4ee7a902d6d30b9f7dd69c878cc63c443ab84ab94b04c57c0e1a77d8bfff55ad14bc8258f69a03196d02f7d54dbc4116c8ae1ae779a923b90405e61202e14082625f454e9602100cd355c48128b91feda0fdde08c0d13c8c1e51fc5bcd4aed80ff33cbf81099651c40380f31aa7dec1c84affa20afcefa01d0aead1e8e4d7d68b8df7ad7b3c82a8ea19137d7899c7b5bde34aac17984429807d37b25e5d19cd2a12ccc58cd02cf041f05fe92f75da3ea0e1ed5e4b0666c3c74bcab179e0d8102ed201c8b94eabf24f30ab78f150e952bb07bf8ed7da2e3d0f7d96168bd794813595c2755bbdeb104fc6ece0767dc06a9390cc92e5fe13c42e71faf8962d42b7309fd5eb1322b186cb8050f91709c5faac7370920f5e8bae24fcb5546ede811347ea05221ca7d90406568ad4fd673aa59d9a0f2d1dec9606374a219302f7a2e4551e90f6cdb8f375776e0fe17684261915c1c9c14b658000b0ba3268e8cedff9741f2fb17f801faf6e07c62d09789926a8418af8d966bfa75fc8e44767696d6820ef6691353f167a21cf6ce200b9ec6b22dd5625b16e21c60827dcc60f25fa4b6a32e9467c0674852e9d7436e36e52029a1e077f77d48527c462f68293fe3665232d51b6b2039d69768fd5ca0193d4021032dab3d3f14a2db85995a3771952131ca927b4568976c1d7aa4a03e53957c181373bca4f904f571fdc43e985ba2c298578ba0ca7a482f23403088f046329763f1e49215df0d86554135bf023bec275cc52b57ccd535ddd03721f64b93e47c37cb27dbd1676ef8d0bb32c58622a27497416250b87fb4305825843bce65416c9cd6e9dfcf4c02369136cbaa457d4d95e34d948a025c8b3ec5006ec427280c1840dccc1f46e09b22882f1275458831593a6dcdf68f326155a0798992ce13b904ef2394e47400973a32254a0da0b6afaf31e5112adee420594f2adadf79548acfba437a4c24fc5bc2381e567abe8bfc30287d99fd9d44c66c194de398978a727548f287bc6581b2a10f2d84a56fe319726c37adcf90bc70744ba3c142b37ab36f9dca17a1edd5ebee61b1104fc351d2fe6e4bbcbfc5da00a756bba88465d889fd4062272dde212400d9133202ee142760df27c2f94f2697b35d81337957e7ec52d71048bf9b8e3d8aefdbb856c9507963bfdbdf1c33b79a70b1424c33e51aa13bf1a335a15a7e41bb18219678ea44f9a1f1bae2c5f72574f39e8cb3b46a2c148d367008fb645b3352f735fde64f5519aae7cd0dd819ecdbeca0789ae9dcf0b88fcd602f49af08601ebb1ee856fd472a707bfccbddfef1bf806841eaecf814de75fee689802a31ecccdf3ddd22ba870e974ddcaebf576dd0200cea0ac842f149b0760b2d867ef0b6252a1090da6f98f5fdf0b0dc5650bf80098b0ed4f4ba02ff43c0e687a4128c8a929cc94fe2c38e582bae3f3cee322f7e045278c67994f41ae190f25c09fb480abc4a94f0917fbfb24"
    bytestream = "e800000001081d5b0380bd0c390708a3507dc3a212c5e6401acfeb7ca8acdfd13ffe086c5264f308a13e6b3e5c71b5b7c1c5ac"
    
    # prompt = f"This is the grammar for the QUIC packet in the RFC 9000 document:\n{contents}\n \nI have this bytestream: {bytestream}.\nExtract each field given in the grammar from the bytestream\n"
    prompt = f"According to the grammar for the QUIC packet in the RFC 9000 document: \nI have this bytestream: {bytestream}.\nExtract each field given in the grammar from the bytestream\n"
    
    return prompt

def read_and_generate_prompts(folder_path):
    contents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            packet_description = file.read()
            follow_up_prompt = generate_follow_up_prompt(packet_description)
            contents.append(follow_up_prompt)
    
    # print(contents)
    return contents

print("Now generating packets...")

# Generate prompts 1b
folder_path = 'output/packettest'
output1b = read_and_generate_prompts(folder_path)
# for i, output in enumerate(output1b):
#     print(i, '\n',output,'\n')
    # if (i < 1):
    #     for item in output:
    #         print(item)

folder_path = 'output/packetadd'
# Write the prompts to new files and send to chatgpt
for i, follow_up_prompt in enumerate(output1b, start=1):
    prompt_path = os.path.join('output/packetadd', f'followup_prompt{i}.txt')
    # print(follow_up_prompt)
    
    #Sending prompt to chatgpt
    initial_message = {
        "role": "system",
        "content": f"{follow_up_prompt}"
    }

    gpt_prompt = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [initial_message],
        temperature=0.5,
        max_tokens=1600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    #Extract output
    output = str(gpt_prompt.choices[0].message.content)
    file_path = os.path.join('output/packetadd', f'output{i}.txt')
    with open(file_path, 'w') as f:
        f.write(output)
    
    #Writing prompts to new file
    with open(prompt_path, 'w') as file:
        file.write(follow_up_prompt)


print("Testing complete")
