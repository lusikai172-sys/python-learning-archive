"""生成与各脚本字段结构一致的「合成数据」，用于在没有原始数据时跑通代码。

背景：本仓库多数脚本依赖课程平台发放的 Excel / 爬虫抓取的文本，这些数据
或因体积、或因版权、或因含个人信息无法随仓库分发。此脚本按各脚本实际读取的
列名与数据类型，生成**结构一致、分布近似、内容虚构**的数据，让克隆者可以先
把流程跑通，再替换成自己的真实数据。

所有数据均由固定随机种子生成，不含任何真实个人或业务信息。

用法：
    python tools/simulate_data.py --list              # 查看可生成的数据集
    python tools/simulate_data.py --dataset all       # 全部生成
    python tools/simulate_data.py --dataset trips     # 只生成网约车行程
    python tools/simulate_data.py --dataset all --rows 5000 --seed 7

默认写到各项目自己的 data/ 目录；已存在的文件不会被覆盖（加 --force 强制覆盖）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------
# 1. 课程作业：数据仓库实训（关联规则 / 回归 / 客户价值 / 信用卡营销）
# --------------------------------------------------------------------------
def ds_warehouse_finance(out: Path, rng: np.random.Generator, n: int) -> str:
    """金融产品购买记录，对应 work01_01.py 的 apriori 输入。

    按「常用套餐」组合生成，而不是纯随机搭配——随机组合下两两共现的支持度
    低于脚本设定的 0.05 下限，挖不出规则。
    """
    bundles = [
        ["理财通", "基金定投"],
        ["信用卡", "消费贷"],
        ["定期存款", "理财通"],
        ["保险", "基金定投", "理财通"],
        ["黄金", "定期存款"],
        ["外汇", "基金定投"],
    ]
    weights = np.array([0.26, 0.22, 0.18, 0.15, 0.11, 0.08])
    rows = []
    for _ in range(n):
        rows.append({"购买产品": ",".join(bundles[rng.choice(len(bundles), p=weights)])})
    _write_table(pd.DataFrame(rows), out)
    return "购买产品（按套餐组合出现，逗号分隔）"


def ds_warehouse_tcm(out: Path, rng: np.random.Generator, n: int) -> str:
    """中医辨证症状组合，对应 work01_02.py 的 FP-Growth 输入。

    症状不为独立随机，而是按证型成组出现——否则各症状支持度都低于 0.05，
    频繁项集会为空、挖掘不出任何规则。
    """
    syndromes = {
        "风寒感冒": ["发热", "畏寒", "头痛", "无汗", "鼻塞"],
        "风热感冒": ["发热", "咽痛", "咳嗽", "口干", "痰黄"],
        "脾胃虚弱": ["纳差", "腹胀", "乏力", "便溏", "面色萎黄"],
        "阴虚火旺": ["盗汗", "口干", "失眠", "舌红", "五心烦热"],
        "心神不宁": ["失眠", "心悸", "乏力", "健忘", "多梦"],
    }
    names = list(syndromes)
    weights = np.array([0.24, 0.22, 0.2, 0.18, 0.16])
    rows = []
    for _ in range(n):
        s = syndromes[rng.choice(names, p=weights)]
        k = int(rng.integers(3, len(s) + 1))
        rows.append({"病人症状": ",".join(rng.choice(s, k, replace=False))})
    _write_table(pd.DataFrame(rows), out)
    return "病人症状（按证型成组出现，逗号分隔）"


def ds_warehouse_income(out: Path, rng: np.random.Generator, n: int) -> str:
    """工龄-薪水，对应 work02_01.py 的一元多项式回归。"""
    years = rng.integers(0, 36, n)
    salary = 4200 + 780 * years + rng.normal(0, 2200, n) + 1.9 * years ** 2
    df = pd.DataFrame({"工龄": years, "薪水": np.round(np.clip(salary, 3000, None), 0)})
    _write_table(df, out)
    return "工龄 / 薪水"


def ds_warehouse_customer(out: Path, rng: np.random.Generator, n: int) -> str:
    """客户价值，对应 work02_02.py 的相关性热力图 + 多项式特征。

    学历按 1=高中及以下 2=专科 3=本科 4=硕士及以上 编码，性别按 0=女 1=男 编码，
    与原始数据的数值化口径一致（见 04_resources/data/DATA.md）。
    """
    edu = rng.choice([1, 2, 3, 4], n, p=[0.2, 0.3, 0.42, 0.08])
    income = np.clip(rng.normal(12000, 5200, n), 2500, None)
    loans = np.round(np.clip(rng.gamma(2.0, 6.0, n), 0, 60), 0)
    amount = np.round(np.clip(loans * rng.normal(38000, 12000, n), 0, None), -3)
    value = np.round(np.clip(0.00004 * amount + 0.02 * income + 0.4 * loans
                             + rng.normal(0, 1.2, n), 0, None), 2)
    df = pd.DataFrame({
        "历史贷款金额": amount,
        "贷款次数": loans,
        "学历": edu,
        "月收入": np.round(income, 0),
        "性别": rng.choice([0, 1], n),
        "客户价值": value,
    })
    _write_table(df, out)
    return "历史贷款金额 / 贷款次数 / 学历 / 月收入 / 性别 / 客户价值"


def ds_warehouse_credit(out: Path, rng: np.random.Generator, n: int) -> str:
    """信用卡精准营销，对应 work03_01.py 的决策树二分类。"""
    income = np.clip(rng.normal(15000, 6000, n), 3000, None)
    spend = np.clip(income * rng.uniform(0.1, 0.6, n), 100, None)
    age = rng.integers(22, 60, n)
    cards = rng.integers(1, 8, n)
    logit = -3.2 + 0.00008 * income + 0.00004 * spend - 0.01 * age + 0.15 * cards
    resp = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    df = pd.DataFrame({
        "年龄": age,
        "月收入": np.round(income, 0),
        "月消费额": np.round(spend, 0),
        "持有信用卡数": cards,
        "性别": rng.choice(["男", "女"], n),
        "响应": resp,
    })
    _write_table(df, out)
    return "年龄 / 月收入 / 月消费额 / 持有信用卡数 / 性别 / 响应"


# --------------------------------------------------------------------------
# 2. 练习：可视化（网约车行程 / 地震数据）
# --------------------------------------------------------------------------
def ds_trips(out: Path, rng: np.random.Generator, n: int) -> str:
    """网约车订单时间戳，对应 visualization/new.py 的小时分布柱状图。"""
    base = dt.datetime(2024, 3, 1)
    hours = rng.choice(np.arange(24), n, p=_commute_profile())
    minute = rng.integers(0, 60, n)
    day = rng.integers(0, 90, n)
    ts = [base + dt.timedelta(days=int(d), hours=int(h), minutes=int(m))
          for d, h, m in zip(day, hours, minute)]
    df = pd.DataFrame({
        "order_id": [f"T{i:07d}" for i in range(n)],
        "start_time": [t.strftime("%Y-%m-%d %H:%M:%S") for t in ts],
        "distance_km": np.round(np.clip(rng.gamma(2.5, 3.4, n), 0.4, 80), 2),
    })
    _write_csv(df, out, encoding="utf-8")
    return "order_id / start_time / distance_km"


def _commute_profile() -> np.ndarray:
    """早晚高峰双峰的 24 小时分布。"""
    p = np.array([0.6, 0.4, 0.3, 0.2, 0.3, 0.8, 2.0, 4.5, 6.0, 3.8, 2.6, 2.8,
                  3.2, 2.9, 2.7, 3.0, 3.6, 4.8, 6.2, 5.0, 3.6, 2.6, 1.6, 0.9])
    return p / p.sum()


def ds_quake(out: Path, rng: np.random.Generator, n: int) -> str:
    """地震目录，对应 visualization/zhengli.py 的震级回归。"""
    start = dt.datetime(2012, 1, 1)
    days = np.sort(rng.integers(0, 4700, n))
    times = [(start + dt.timedelta(days=int(d),
                                   hours=int(rng.integers(0, 24)),
                                   minutes=int(rng.integers(0, 60)))).strftime("%Y-%m-%d %H:%M:%S")
             for d in days]
    lat = np.round(np.clip(rng.normal(31.5, 9.0, n), 18, 53), 2)
    lon = np.round(np.clip(rng.normal(104.0, 12.0, n), 73, 135), 2)
    depth = np.round(np.clip(rng.gamma(2.0, 6.5, n), 1, 600), 0)
    mag = np.round(np.clip(rng.normal(3.1, 0.7, n) + 0.0015 * depth, 1.0, 8.0), 1)
    df = pd.DataFrame({
        "发震时刻": times,
        "纬度(°)": lat,
        "经度(°)": lon,
        "深度(千米)": depth,
        "震级(M)": mag,
        "参考位置": [f"北纬{v:.1f}° 东经{u:.1f}° 区域{rng.integers(1, 30)}" for v, u in zip(lat, lon)],
    })
    _write_table(df, out)
    return "发震时刻 / 纬度(°) / 经度(°) / 深度(千米) / 震级(M)"


# --------------------------------------------------------------------------
# 3. 研究项目（课程评论 BERTopic / 评教数据 / 旅游政策 LDA）
# --------------------------------------------------------------------------
_COURSE_PHRASES = [
    "老师讲课条理清晰，案例贴近实际，收获很大",
    "课程内容偏理论，希望增加一些实操环节",
    "作业量适中，批改很及时，反馈很有帮助",
    "课堂互动比较多，能带动思考",
    "课件更新不够及时，有些内容和教材对不上",
    "考核方式比较合理，平时分和期末各占一半",
    "老师很负责，课后答疑很耐心",
    "课程难度偏大，零基础听起来有些吃力",
    "小组作业分工不太均衡，希望加强过程管理",
    "案例教学效果好，能理解抽象的管理概念",
    "希望多讲一些数据分析工具的实际应用",
    "课程节奏偏快，部分章节来不及消化",
    "课堂氛围轻松，愿意主动回答问题",
    "教材选择一般，建议补充最新的行业报告",
    "实验课安排合理，动手之后理解更深",
    "考试重点明确，复习方向比较清楚",
]


def ds_course_review(out: Path, rng: np.random.Generator, n: int) -> str:
    """课程评论，对应 course-review-topic-modeling/preprocess_comments.py。"""
    texts = []
    for _ in range(n):
        k = int(rng.integers(1, 3))
        texts.append("，".join(rng.choice(_COURSE_PHRASES, k, replace=False)) + "。")
    _write_table(pd.DataFrame({"评论": texts}), out)
    return "评论（单列中文短文本）"


def ds_teaching(out: Path, rng: np.random.Generator, n: int) -> str:
    """评教明细，对应 teacher_review_analysis.py（无表头，gbk 编码）。

    列序：姓名, 总分, 院系, question_1..question_12
    """
    depts = ["管理科学与工程学院", "商学院", "计算机与网络安全学院", "文法学院", "旅游与城乡规划学院"]
    names = [f"教师{i:03d}" for i in range(1, 61)]
    rows = []
    for _ in range(n):
        q = np.round(np.clip(rng.normal(88, 6, 12), 60, 100), 1)
        rows.append([rng.choice(names), round(float(q.mean()), 2), rng.choice(depts), *q])
    df = pd.DataFrame(rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, header=False, index=False, encoding="gbk")
    return "name / score / department / question_1..12（无表头，gbk）"


_POLICY_SECTIONS = [
    "第一章 总则。为规范和加强天府旅游名县命名县管理，推动县域文化旅游高质量发展，制定本细则。",
    "第二章 申报条件。申报县应当具备良好的旅游资源禀赋，拥有较为完善的旅游公共服务设施和旅游交通体系。",
    "第三章 评选程序。按照自愿申报、市级初审、省级复核、专家评审、社会公示的程序组织实施。",
    "第四章 动态管理。命名县实行动态管理，每三年进行一次复核，对复核不达标的限期整改。",
    "第五章 支持政策。省级文化和旅游发展专项资金对命名县给予倾斜支持，优先安排旅游基础设施项目。",
    "第六章 品牌建设。鼓励命名县培育地方文旅品牌，发展乡村旅游、康养旅游、研学旅游等新业态。",
    "第七章 附则。本细则由省文化和旅游厅负责解释，自发布之日起施行。",
]

# 通用政策高频词：任何一份旅游政策文本都会大量出现，用来保证词频统计有意义
_POLICY_COMMON = [
    "旅游", "服务", "管理", "政策", "项目", "资金", "发展", "保护", "规划", "标准",
    "体系", "机制", "平台", "品牌", "创新", "监管", "生态", "融合", "安全", "满意度",
    "宣传", "推广", "考核", "评估", "培训", "支持", "完善", "提升", "优化", "落实",
]

_POLICY_PATTERNS = [
    "{a}与{b}要同步推进，健全{c}，明确{d}责任，提升{e}水平。",
    "围绕{a}，完善{b}和{c}，强化{d}，形成可考核的{e}。",
    "在{a}方面，应当统筹{b}，优化{c}配置，加强{d}与{e}的衔接。",
    "支持依托{a}发展{b}，推动{c}下沉，落实{d}和{e}要求。",
    "对{a}实行清单化管理，健全{b}，定期开展{c}评估，强化{d}和{e}。",
]


def ds_policy_docx(out: Path, rng: np.random.Generator, n: int) -> str:
    """政策文本 docx，对应 provincial-tourism-lda/*.py 的输入（无第三方依赖写 docx）。

    词汇取自同目录下的 `*tourism_dict*.txt` 自定义词典（不足时补通用政策词）：
    LDA 脚本只保留词典词与白名单词，纯自由造句会导致词表为空、模型报错。
    """
    vocab = []
    for f in sorted(out.parent.glob("*tourism_dict*.txt")):
        vocab += [w.strip().split()[0] for w in f.read_text(encoding="utf-8").splitlines() if w.strip()]
    vocab = vocab or _POLICY_COMMON
    pool = vocab + _POLICY_COMMON

    paras = list(_POLICY_SECTIONS)
    for i in range(60):
        tpl = _POLICY_PATTERNS[i % len(_POLICY_PATTERNS)]
        words = rng.choice(pool, 5, replace=False)
        paras.append(f"第{i + 1}条 " + tpl.format(**dict(zip("abcde", words))))
    _write_docx(out, paras)
    return f"政策条文段落（合成，{len(paras)} 段，词典词 {len(vocab)} 个）"


# --------------------------------------------------------------------------
# 落盘工具
# --------------------------------------------------------------------------
def _write_table(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")


def _write_csv(df: pd.DataFrame, path: Path, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding=encoding)


def _write_docx(path: Path, paragraphs: list[str]) -> None:
    """写一个最小可用的 .docx（word/document.xml + 必要关系），免装 python-docx。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(
        f'<w:p><w:r><w:t xml:space="preserve">{escape(p)}</w:t></w:r></w:p>' for p in paragraphs
    )
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{body}</w:body></w:document>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document.main+xml"/></Types>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)


# --------------------------------------------------------------------------
# 数据集注册表
# --------------------------------------------------------------------------
DATASETS = {
    # key: (相对路径, 生成函数, 默认行数, 面向的脚本, 说明)
    "finance": ("01_coursework/data-warehouse/data/金融产品购买数据.xlsx",
                ds_warehouse_finance, 3000, "work01_01.py", "关联规则 - 商品组合"),
    "tcm": ("01_coursework/data-warehouse/data/中医辨证.xlsx",
            ds_warehouse_tcm, 2000, "work01_02.py", "关联规则 - 症状组合"),
    "income": ("01_coursework/data-warehouse/data/行业收入表-餐饮服务.xlsx",
               ds_warehouse_income, 1200, "work02_01.py", "多项式回归 - 工龄薪水"),
    "customer": ("01_coursework/data-warehouse/data/客户价值数据表.xlsx",
                 ds_warehouse_customer, 1500, "work02_02.py", "相关性分析 - 客户价值"),
    "credit": ("01_coursework/data-warehouse/data/信用卡精准营销模型.xlsx",
               ds_warehouse_credit, 2500, "work03_01.py", "二分类 - 营销响应"),
    "trips": ("02_practice/visualization/data/train_new2.csv",
              ds_trips, 20000, "new.py", "网约车订单小时分布"),
    "quake": ("02_practice/visualization/data/中国地震数据（2012-2024）_ppman.xlsx",
              ds_quake, 6000, "zhengli.py", "地震震级回归"),
    "reviews": ("03_research/course-review-topic-modeling/data/管理类课程评论.xlsx",
                ds_course_review, 3000, "preprocess_comments.py", "课程评论文本"),
    "teaching": ("03_research/teaching-reform-analysis/data/2021-2022-2评教统计明细.csv",
                 ds_teaching, 800, "teacher_review_analysis.py", "评教明细"),
    "policy": ("03_research/provincial-tourism-lda/四川天府旅游命名县（2021年修订）.docx",
               ds_policy_docx, 300, "sichuan.py 等", "旅游政策文本"),
}


def main() -> None:
    ap = argparse.ArgumentParser(description="生成结构一致的合成数据")
    ap.add_argument("--dataset", default="all", help="数据集名（见 --list），或 all")
    ap.add_argument("--list", action="store_true", help="列出可生成的数据集")
    ap.add_argument("--rows", type=int, default=0, help="覆盖默认行数")
    ap.add_argument("--seed", type=int, default=20261121, help="随机种子")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    ap.add_argument("--out-root", default=str(ROOT), help="输出根目录，默认为仓库根")
    args = ap.parse_args()

    if args.list:
        print(f"{'名称':<10}{'默认行数':>8}  {'服务脚本':<26}说明")
        print("-" * 96)
        for key, (_, _, n, script, desc) in DATASETS.items():
            print(f"{key:<10}{n:>8}  {script:<26}{desc}")
        print("\n用法：python tools/simulate_data.py --dataset all")
        return

    keys = list(DATASETS) if args.dataset == "all" else [args.dataset]
    unknown = [k for k in keys if k not in DATASETS]
    if unknown:
        raise SystemExit(f"未知数据集：{unknown}，用 --list 查看可用名称")

    root = Path(args.out_root).resolve()
    rng = np.random.default_rng(args.seed)
    made = skipped = 0
    print(f"输出根目录：{root}\n")
    for key in keys:
        rel, func, n, script, _ = DATASETS[key]
        target = root / rel
        if target.exists() and not args.force:
            print(f"[跳过] {key:<10} 已存在 {rel}")
            skipped += 1
            continue
        note = func(target, rng, args.rows or n)
        print(f"[生成] {key:<10} {rel}")
        print(f"         字段：{note}  →  {script}")
        made += 1

    print(f"\n完成：生成 {made} 个，跳过 {skipped} 个（--force 可覆盖）")
    print("注意：以上均为合成数据，仅用于跑通流程；真实数据请按 DATA.md 的途径获取。")


if __name__ == "__main__":
    main()
