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

template1 = '''
你是一位编剧。你的任务是根据剧目的标题编写剧情简介。
剧目标题：{title}
编剧：这是上述剧目的剧情简介：
'''
prompt1 = PromptTemplate.from_template(template1)
synopsis_chain = LLMChain(llm=llm, prompt=prompt1)

template2 = '''
你是一位来自《纽约时报》的戏剧评论家。根据剧情简介，你的任务是为该剧目撰写一篇评论。
剧情简介：
{synopsis}
来自《纽约时报》的戏剧评论家对上述剧目的评论：
'''
prompt2 = PromptTemplate.from_template(template2)
review_chain = LLMChain(llm=llm, prompt=prompt2)

from langchain.chains import SimpleSequentialChain
sequential_chain = SimpleSequentialChain(chains=[synopsis_chain, review_chain], verbose=True)

review = sequential_chain.run('黄昏海滩上的小女孩和大黄狗')
print(review)



