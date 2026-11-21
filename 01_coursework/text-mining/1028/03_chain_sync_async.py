from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import asyncio
import time


# 同步链
def syn_chains():
    import os
    api_key = os.getenv("ZHIPU_API_KEY")

    llm = ChatOpenAI(
        model="glm-4-flash",
        openai_api_key=api_key,  # 请填写您自己的APIKey
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

    input_list = [{'product':i} for i in ['袜子', '电脑', '鞋子']]
    print(llm_chain.apply(input_list))

    # for i in range(len(input_list)):
    #     resp = llm_chain.invoke({'product':input_list[i]})
    #     print(resp)


# 异步链
async def asy_chain_tool(chain, product):
    resp = await chain.ainvoke({'product':product})
    print(resp)

async def asy_chain():
    import os
    api_key = os.getenv("ZHIPU_API_KEY")

    llm = ChatOpenAI(
        model="glm-4-flash",
        openai_api_key=api_key,  # 请填写您自己的APIKey
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
    )
    template = '''
       我希望你能担任新公司的命名顾问。
       一个制造{product}的公司取什么名字好呢？
       只回复公司名，不回复其他内容。
       '''
    prompt = PromptTemplate.from_template(template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    input_list = ['袜子', '电脑', '鞋子']
    tasks = [asy_chain_tool(llm_chain, input_list[i]) for i in range(len(input_list))]
    await asyncio.gather(*tasks)

start = time.time()
syn_chains()
end = time.time()
print('同步链调用时间：', end - start)

start = time.time()
asyncio.run(asy_chain())
end = time.time()
print('异步链调用时间：', end - start)