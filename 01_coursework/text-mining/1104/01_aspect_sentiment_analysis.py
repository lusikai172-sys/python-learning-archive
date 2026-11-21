import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import asyncio

with open(f'{TEXT_DATA_DIR}/第四章/深度学习评论.txt', 'r', encoding='utf-8') as f:
    texts = [i.strip() for i in f.readlines()]

# 如果你的评论太多，建议拆分为多个块，每块单独跑一次

criteria_and_explain = {
  "课程内容的准确性":"课程内容是否与主题紧密相关，信息准确无误。",
  "课程结构的逻辑性":"课程内容的组织是否条理清晰，逻辑性强。",
  "知识点的覆盖面":"课程是否涵盖了该领域的关键知识点和最新进展。",
  "实用性和应用性":"课程内容是否实用，能否直接应用于实际工作或学习中。",
  "案例和实例的丰富性":"课程中是否包含足够的案例和实例来辅助理解。",
  "教学方法的多样性":"是否采用了多种教学方法（如视频讲解、互动问答、小组讨论等）。",
  "讲解的清晰度与易懂性":"教师的讲解是否清晰易懂，语速和语调是否适中。",
  "互动环节的设置":"课程中是否设置了足够的互动环节，如提问、讨论、小测验等。",
  "个性化学习支持":"是否提供了个性化的学习路径和进度跟踪功能。",
  "反馈机制的及时性":"对于学员的提问和作业，教师或助教是否及时给予反馈。",
  "平台的稳定性与流畅性":"在线学习平台是否稳定，视频播放是否流畅。",
  "用户界面的友好性":"平台的用户界面是否简洁明了，易于操作。",
  "学习资源的丰富性":"除了课程视频外，是否还提供了PPT、讲义、参考文献等学习资源。",
  "移动学习支持":"是否支持移动设备访问，如手机和平板电脑。",
  "技术支持的响应速度":"遇到技术问题时，技术支持团队是否迅速响应并解决问题。",
  "学习目标的达成度":"学员通过学习是否能够达到课程设定的学习目标。",
  "知识掌握程度的提升":"学员在知识掌握、技能提升等方面的进步情况。",
  "课程整体满意度":"学员对课程的整体满意度。",
  "推荐意愿":"学员是否愿意向他人推荐该在线课程。",
  "持续学习意愿":"学员在完成当前课程后，是否有继续学习该领域其他课程的意愿。"

}


import os
api_key = os.getenv("ZHIPU_API_KEY")

llm = ChatOpenAI(
    model="glm-4-flash",
    openai_api_key=api_key,  # 请填写您自己的APIKey
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)
template = '''
   对于评论“{review}”，帮我判断它与方面“{aspect}”是否有关，以及评论关于该方面的情感倾向。
   其中方面“{aspect}”是指“{explain}”。
   如果与该方面无关，直接回复2。
   如果与该方面有关，但是没有明显的情感倾向，回复0。
   如果与该方面有关，且对该方面为正向情感倾向，回复1。
   如果与该方面有关，且对该方面为负向情感倾向，回复-。   
   只回复2，0，1和-1四者之一，不要回复其他内容。
   '''
prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(llm=llm, prompt=prompt)


# 异步链
async def asy_chain_tool(chain, review, aspects):
    input_list = [{'review':review, 'aspect':aspect, 'explain':aspects[aspect]} for aspect in aspects.keys()]
    resp = await chain.aapply(input_list)
    result = {i:resp[index]['text'] for index, i in enumerate(aspects.keys())}
    print(result)
    result = {review:result}
    return result


async def asy_chain():
    tasks = [asy_chain_tool(llm_chain, text, criteria_and_explain) for text in texts]
    # tasks = [asy_chain_tool(llm, file) for file in files]
    results = await asyncio.gather(*tasks)

    return results

results = asyncio.run(asy_chain())