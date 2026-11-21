from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import os
api_key = os.getenv("ZHIPU_API_KEY")

llm = ChatOpenAI(
    model="glm-4-flash",
    openai_api_key=api_key,# 请填写您自己的APIKey
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)
template = '''
我希望你能担任新公司的命名顾问。
一个制造{product}的公司取什么名字好呢？
只回复公司名，不回复其他内容。
'''
prompt = PromptTemplate.from_template(template)

# 用LLMChain创建对话工具，该工具会自动更新记忆，不需要重复创建，手动更新
llm_chain = LLMChain(llm=llm, prompt=prompt)
# LCEL
# llm_chain = prompt | llm

input_list = [{'product':i} for i in ['袜子', '电脑', '鞋子']]
result_list = llm_chain.apply(input_list)
print(result_list)


