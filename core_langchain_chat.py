#内置库
import os
import json
#第三方库
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict

load_dotenv("qwen_key.env")
model = ChatDeepSeek(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    streaming = True
)
str_parser = StrOutputParser()

#================================13本地文件对话记忆================================
class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path) -> None:
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(storage_path,session_id)
        os.makedirs(self.storage_path,exist_ok=True)

    def add_messages(self,messages) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        new_messages = []
        for message in all_messages:
            d = message_to_dict(message)
            new_messages.append(d)

        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)

    @property
    def messages(self):
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                loaded_json =  json.load(f)
                return messages_from_dict(loaded_json)
        except FileNotFoundError:
            return []

    def clear(self):
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)

#==========================创建基础链=======================
prompt = ChatPromptTemplate.from_messages([
    ("system","""
# 角色定位
你是专业的科创研究数据处理助手，专注植物香气对注意力影响实验的数据分析与代码生成。

# 项目背景
本次实验研究三种植物香气（丁香、薰衣草、雪松）对人体注意力的影响，
共150名志愿者分为三组，每周闻香气5次、每次20分钟；
采用舒尔特方格、Stroop 任务用时作为注意力评价指标，
实验包含前测与多轮后测，完整周期1个月，现已完成全部数据采集。

# 数据文件说明
1. Stroop 数据文件
路径：/Users/pc/Desktop/longtitudinal_comparison/stroop_多次对比.xlsx
字段：id、name、0～8
含义：0=前测，1-8为历次后测，空值代表无效数据；
一行对应一名受试者多次测试平均值，每人测试次数 2～9 次不等。

2. Schulte 数据文件
路径：/Users/pc/Desktop/longtitudinal_comparison/schulte_多次对比.xlsx
字段结构、测试规则、分组逻辑与 Stroop 文件完全一致。

# 分组规则
id 为三位数，百位代表组别：
1 = 丁香组
2 = 薰衣草组
3 = 雪松组

# 工作要求
1. 因LLM无法直接读取本地Excel文件，需生成**可直接复制独立运行**的完整Python代码；
2. 自动忽略空值、过滤无效数据，按组别拆分分析；
3. 输出代码结构清晰、注释完善、可直接用于后续统计与绘图；
4. 严格基于给定实验背景与字段规则作答，不自行编造实验条件。

# 对话规则
结合历史对话上下文理解用户当前问题，基于以上全部设定给出专业、准确、可落地的回答与代码。
    """),
    ("user","请你根据历史信息回答问题。历史信息是{history},用户问题是{input}")
])

base_chain = prompt | model

#=============================创建增强链==========================
def get_history(session_id):
    storage_path = os.path.join(os.path.dirname(__file__), "chat_history")
    return FileChatMessageHistory(session_id, storage_path)

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    history_messages_key = "history",
    input_messages_key = "input"
)

#================================主程序运行==============================
if __name__ == "__main__":
    print("="*124)
    print(" "*40,"🌿 科创数据助手已启动（输入问题后，输 end 发送）")
    print(" "*46,"🚪 输入 quit / exit 可退出程序")
    print("="*124)

    session_config = {
        "configurable": {"session_id": "003"}
    }

    while True:
        print("输入问题后，换行输入end，再换行即可发送问题:")

        # 多行输入读取
        lines = []

        #======================无限循环的作用：python以回车为标志，自动按行切割遍历每一行==============
        while True:
            line = input()

            # 先判断是否要退出指令
            if line.strip().lower() in ["quit", "exit", "q", "退出"]:
                print("\n👋 程序已退出，记忆已保存")
                exit()

            # 再判断是否要结束输入
            if line.strip().lower() == "end":
                break

            #如果都不是，则line追加到lines，进入下一循环处理下一行
            lines.append(line)

        user_input = "\n".join(lines)

        # 空内容跳过
        if not user_input.strip():
            print("⚠️ 输入不能为空，请重新输入")
            continue

        # 获取回答
        try:
            print("\n🤖 助手回答：")
            # 直接 for 循环 stream，不要用变量接
            for chunk in conversation_chain.stream(
                    {"input": user_input},
                    config=session_config
            ):
                print(chunk.content, end="", flush=True)
            print()
        except Exception as e:
            print("\n❌ 运行出错：", e)

        print("-"*60)
        print()
        print()