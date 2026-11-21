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
你是一位擅长喜剧的编剧。你的任务是根据剧目的标题编写一个类型为喜剧的剧情简介。
剧目标题：{title}
编剧：这是上述剧目的剧情简介：
'''
prompt1 = PromptTemplate.from_template(template1)
chain1 = LLMChain(llm=llm, prompt=prompt1, output_key='comedy')

template2 = '''
你是一位擅长悲剧的编剧。你的任务是根据剧目的标题编写一个类型为悲剧的剧情简介。
剧目标题：{title}
编剧：这是上述剧目的剧情简介：
'''
prompt2 = PromptTemplate.from_template(template2)
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key='tragedy')


template3 = '''
你是一位{personality}戏剧评论家。根据剧情简介，你的任务是为给你的剧目撰写评论。
接下来，我会给你两个剧目，剧目1：
{comedy}
剧目2：
{tragedy}
请对上面的两个剧目做出评论，并指出这两个剧目哪个你更看好，并说明原因：
'''
prompt3 = PromptTemplate.from_template(template3)
chain3 = LLMChain(llm=llm, prompt=prompt3, output_key='review')

from langchain.chains import SequentialChain
sequential_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=['title', 'personality'],
    output_variables=['comedy', 'tragedy', 'review'],
    verbose=True)

review = sequential_chain.invoke({'title':'黄昏海滩上的小女孩和大黄狗', 'personality':'幽默的'})
print(review)



