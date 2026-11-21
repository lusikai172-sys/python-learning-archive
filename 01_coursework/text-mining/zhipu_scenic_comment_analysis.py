import pandas as pd
from zhipuai import ZhipuAI
import re
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


# 读取Excel文件中的景区评论数据
def read_comment_data(file_path):
    """
    读取指定路径的Excel文件中的景区评论数据

    :param file_path: Excel文件的路径
    :return: 含景区评论数据的DataFrame
    """
    return pd.read_excel(file_path)


# 分析景区评论在各个评价标准方面的情感倾向
def analyze_comment_sentiment(client, line, evaluation_criteria):
    prompt = f'''
    帮我分析景区评论"{line}"中关于 {evaluation_criteria} 共10个方面的情感倾向及是否涉及该方面。
    包含3种情况，正面、负面、不涉及该方面，分别用1、-1和0表示。
    请一步步思考作出回答，每步仅考虑该景区评论中关于一个方面的情感倾向。
    请给出完整的结果。用列表的形式回复结果，如假设存在某个评论关于交通便利性是负面评价，关于其他方面不涉及，则回复为[0, -1, 0, 0, 0, 0, 0, 0, 0, 0]，列表中元素的顺序与10个方面的序一一对应。
    请你只回复该列表，不要回复其他内容。
    '''
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    answers = []
    for chunk in response:
        if chunk.choices[0].delta.content:
            answers.append(chunk.choices[0].delta.content)
    try:
        return json.loads(''.join(answers))
    except json.JSONDecodeError as e:
        print(f"解析智谱AI响应内容时出错: {e}")
        return None


# 从文本文件中提取情感倾向分析结果并整理成DataFrame
def extract_results_from_text(text_file_path):
    """
    从指定路径的文本文件中提取以列表形式表示的情感倾向分析结果，并整理成DataFrame

    :param text_file_path: 存储情感倾向分析结果的文本文件路径
    :return: 含情感倾向分析结果的DataFrame
    """
    with open(text_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'\[.*?\]'
    matches = re.findall(pattern, content)

    df = pd.DataFrame({'multi_comment': matches})
    return df


# 处理DataFrame中的数据格式，确保数据可用
def process_dataframe(df):
    """
    处理DataFrame中的数据格式，将字符串形式的数列转换为实际的列，并去除包含空值的行

    :param df: 含情感倾向分析结果的DataFrame
    :return: 处理好的数据格式的DataFrame
    """
    def safe_json_loads(s):
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            return None

    df['multi_comment'] = df['multi_comment'].apply(safe_json_loads)
    df = df.dropna(subset=['multi_comment'])
    df = df.reset_index(drop=True)
    return df


# 计算每个评价标准方面的满意度和关注度
def calculate_satisfaction_and_attention(df, evaluation_criteria):
    """
    计算每个评价标准方面的满意度和关注度

    :param df: 含情感倾向分析结果的DataFrame
    :param evaluation_criteria: 评价标准列表
    :return: 含每个评价标准方面的满意度和关注度结果的DFrame
    """
    def sense(i, comment_count):
        total_count = ((df['multi_comment'].apply(lambda x: x[i]) == 1) |
                       (df['multi_comment'].apply(lambda x: x[i]) == -1)).sum()
        satisfaction = sum(row[i] == 1 for row in df['multi_comment'])/total_count
        attention = total_count/comment_count
        return satisfaction, attention

    comment_count = len(df)
    result_dict = {}
    for index, value in enumerate(evaluation_criteria):
        satis, atten = sense(index, comment_count)
        result_dict[value] = {'满意度': satis, '关注度': atten}

    return pd.DataFrame.from_dict(result_dict, orient='index')


if __name__ == "__main__":
    # 1. 读取景区评论数据
    file_path = DATA_DIR / "同程_峨眉山评论.xlsx"
    df = read_comment_data(file_path)

    evaluation_criteria = ["景观美感", "交通便利性", "环境卫生", "服务设施", "门票价格合理性", "游客密度", "入内人员限制", "文化体验", "食宿条件", "游览路线设计"]

    # 2. 初始化智谱AI客户端（需日前填入自己的API Key）
    api_key = os.environ.get("ZHIPUAI_API_KEY", "")
    if not api_key:
        raise SystemExit("请先设置环境变量 ZHIPUAI_API_KEY（原脚本中的明文 Key 已移除，请使用自己的 Key）")
    client = ZhipuAI(api_key=api_key)

    # 3. 分析每条评论的情感倾向并将结果写入xlsx文件
    text_file_path = Path(__file__).resolve().parent / "小组作业方面级情感分析_1.txt"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file_path = OUTPUT_DIR / "情感分析结果.xlsx"
    result_df = pd.DataFrame(columns=evaluation_criteria)

    for index, line in enumerate(df['内容']):
        answers = analyze_comment_sentiment(client, line,  evaluation_criteria)
        if answers is not None:
            # 将列表形式的答案转换为字符串后再存入DataFrame
            result_df.loc[index, 'multi_comment'] = json.dumps(answers)
            print(answers)
        else:
            print(f"分析评论 {index} 时未获取到有效结果")

    result_df.to_excel(output_file_path, index=False)

    # 4. 处理DataFrame中的数据格式（这里直接使用之前处理函数对新生成的结果DataFrame进行处理）
    result_df = process_dataframe(result_df)

    # 5. 计算每个评价标准方面的满意度和关注度，并保存到xlsx文件
    satisfaction_attention_df = calculate_satisfaction_and_attention(result_df, evaluation_criteria)
    satisfaction_attention_output_path = OUTPUT_DIR / "满意度和关注度结果.xlsx"
    satisfaction_attention_df.to_excel(satisfaction_attention_output_path)