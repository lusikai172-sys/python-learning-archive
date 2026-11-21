import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("WAREHOUSE_DATA_DIR", Path(__file__).resolve().parent / "data"))

import pandas as pd
from apyori import apriori


# 读取金融产品购买数据并整理为算法可识别的格式
def read_and_prepare_data(file_path):
    df = pd.read_excel(file_path)

    # 处理购买产品列数据，去除可能存在的空格并按逗号分割成列表
    transactions = df["购买产品"].str.strip().str.split(",", expand=False).tolist()

    return transactions


# 设置不同组的参数并进行关联规则挖掘
def perform_association_rule_mining(transactions, min_support_range, min_confidence_range, lift_threshold_range):
    all_results = []

    for min_support in min_support_range:
        for min_confidence in min_confidence_range:
            for lift_threshold in lift_threshold_range:
                rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence)
                results = list(rules)

                for i in results:
                    for j in i.ordered_statistics:
                        X = j.items_base
                        Y = j.items_add
                        x = ', '.join([item for item in X])
                        y = ', '.join([item for item in Y])
                        if x!= '':
                            support = i.support
                            confidence = j.confidence
                            lift = j.lift
                            if lift >= lift_threshold:
                                rule = {
                                    "support": support,
                                    "confidence": confidence,
                                    "lift": lift,
                                    "base": x,
                                    "add": y
                                }
                                all_results.append(rule)

    return all_results


# 结构化显示挖掘的关联规则
def display_association_rules(results):
    print(f"| {'support':<10} | {'confidence':<10} | {'lift':<10} | {'base':<30} | {'add':<30} |")
    print("|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 12 + "|" + "-" * 32 + "|" + "-" * 32 + "|")

    for result in results:
        print(f"| {result['support']:<10.4f} | {result['confidence']:<10.4f} | {result['lift']:<10.4f} | {result['base']:<30} | {result['add']:<30} |")


if __name__ == "__main__":
    file_path = DATA_DIR / "金融产品购买数据.xlsx"

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