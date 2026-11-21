import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("WAREHOUSE_DATA_DIR", Path(__file__).resolve().parent / "data"))

import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules


# 读取中医辨证数据并整理为算法可识别的格式
def read_and_prepare_data(file_path):
    df = pd.read_excel(file_path)
    # 将“病人症状”列的数据按逗号分割并转换为列表形式
    transactions = df["病人症状"].str.split(",", expand=False).tolist()
    # 创建一个新的 DataFrame，将每个症状转换为布尔值
    new_df = pd.DataFrame()
    unique_symptoms = set(item for sublist in transactions for item in sublist)
    for symptom in unique_symptoms:
        new_df[symptom] = [symptom in sublist for sublist in transactions]
    return new_df


# 进行关联规则挖掘
def perform_association_rule_mining(transactions, min_support_range, min_confidence_range, lift_threshold_range):
    all_results = []
    for min_support in min_support_range:
        for min_confidence in min_confidence_range:
            for lift_threshold in lift_threshold_range:
                # 使用 fp-growth 算法找出频繁项集
                frequent_itemsets = fpgrowth(transactions, min_support=min_support, use_colnames=True)
                # 根据频繁项集和最小置信度生成强关联规则
                rules = association_rules(frequent_itemsets, min_threshold=min_confidence)
                for _, rule in rules.iterrows():
                    antecedents = ', '.join([item for item in rule['antecedents']])
                    consequents = ', '.join([item for item in rule['consequents']])
                    support = rule['support']
                    antecedent_support = rule['antecedent support']
                    consequent_support = rule['consequent support']
                    lift = rule['lift']
                    leverage = rule['leverage']
                    conviction = rule['conviction']
                    if lift >= lift_threshold:
                        result = {
                            "antecedents": antecedents,
                            "consequents": consequents,
                            "support": support,
                            "antecedent support": antecedent_support,
                            "consequent support": consequent_support,
                            "leverage": leverage,
                            "lift": lift,
                            "conviction": conviction
                        }
                        all_results.append(result)
    return all_results


# 结构化显示挖掘的关联规则
def display_association_rules(results):
    print(f"| {'antecedents':<20} | {'consequents':<20} | {'support':<10} | {'antecedent support':<20} | {'consequent support':<20} | {'leverage':<10} | {'lift':<10} | {'conviction':<10} |")
    print("|" + "-" * 22 + "|" + "-" * 22 + "|" + "-" * 12 + "|" + "-" * 22 + "|" + "-" * 22 + "|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 12 + "|")
    for result in results:
        print(f"| {result['antecedents']:<20} | {result['consequents']:<20} | {result['support']:<10.4f} | {result['antecedent support']:<20.4f} | {result['consequent support']:<20.4f} | {result['leverage']:<10.4f} | {result['lift']:<10.4f} | {result['conviction']:<10.4f} |")


if __name__ == "__main__":
    file_path = DATA_DIR / "中医辨证.xlsx"
    # 读取并整理数据
    transactions = read_and_prepare_data(file_path)
    # 设置多组参数尝试
    min_support_range = [i/100 for i in range(5, 30, 5)]
    min_confidence_range = [i/100 for i in range(30, 80, 10)]
    lift_threshold_range = [i/10 for i in range(10, 20)]
    # 进行关联规则挖掘
    results = perform_association_rule_mining(transactions, min_support_range, min_confidence_range, lift_threshold_range)
    # 显示挖掘的关联规则
    display_association_rules(results)