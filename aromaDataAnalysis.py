from openai import OpenAI
from dotenv import load_dotenv,find_dotenv
import os

#===========1、key与client===========
load_dotenv(find_dotenv())
client = OpenAI(
    api_key = os.get("deepseek_key.env"),
    base_url = "https://api.deepseek.com"
)



#===========2、系统提示词SYSTEM_PROMPT===========
SYSTEM_PROMPT = "你是一个数据分析专家......"



#===========3、用户提示词USER_PROMPT===========
USER_PROMPT = """{
    user_input
}"""



#===========4、定义get_prompt===========
def get_prompt(user_input):
    prompt = [
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":user_input},
    ]
    return prompt



#===========5、定义get_completion===========
def get_completion(model="deepseek-chat",messages=prompt,temperature=0.1):
    response = client.chat.completion.create(
     model = model,
     messages = prompt,
     temperature = 0.1
)
    return response.choices[0].messages.content



#===========6、输出结果===========
if __name__ == "__main__":
    user_input = "此处待键入指令"
    prompt = get_prompt(user_input)
    result = get_complition(prompt)
    print(result)