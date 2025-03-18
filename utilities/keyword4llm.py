
from openai import OpenAI
import requests
import json 

keyword_prompt='''
System message:

Your input fields are:
1. `text` (str)

Your output fields are:
1. `q` 

All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## text ## ]]
{text}

[[ ## q ## ]]
{q} # note: Optional Parameters in the Query: [
    {"Parameter": "type","Type": "string","Description": "Type, can be 'user' or 'org', representing individual users and organizations respectively."},
    {"Parameter": "in","Type": "string","Description": "Search within which attribute, can be 'login', 'email', 'fullname', or a combination thereof, representing the login username, email address, and full name respectively."},
]

[[ ## completed ## ]]

In adhering to this structure, your objective is: 
        Given a customer inquiry or complaint in the text field, predict the most appropriate `q` for searching GitHub repositories.


User message:

[[ ## text ## ]]
人工智能

Response:

[[ ## q ## ]]
in:name artificial%20intelligence OR in:description machine%20learning
[[ ## completed ## ]]

'''

class KeyWord4Llm:
    def __init__(self, api_key, base_url, model ):

        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def get_keyword(self, query):

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": keyword_prompt
                },
                {
                    "role": "user", 
                    "content": f"{query}"
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "stop": None,
            "temperature": 0.9,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", self.base_url, json=payload, headers=headers)
        
        
        response_dict=json.loads(response.text)
        ret = response_dict['choices'][0]['message']['content']

        # 方法1：通过查找特定标记并提取下一行内容
        lines = ret.strip().splitlines()

        for i, line in enumerate(lines):
            if '## q ##' in line:
                # 下一行即为 q 的值
                q_value = lines[i + 1].strip()
                print(q_value)
                return q_value
        else:
            print("No match found")
            return "No match found"



        

# 示例调用
if __name__ == '__main__':
    keyword4llm = KeyWord4Llm(api_key="你的key",
                              base_url="https://api.siliconflow.cn/v1/chat/completions",
                              model="Qwen/Qwen2.5-7B-Instruct"
                              )  # 如果需要认证，请提供您的个人访问令牌

    ret = keyword4llm.get_keyword(query="大语言模型")

    print(ret)
    # 使用正则表达式提取 q 的值

