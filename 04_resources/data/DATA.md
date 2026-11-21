# 数据获取与模拟指南

本仓库的代码大多依赖课程平台发放的表格、网站抓取的文本或调研数据。这些原始数据
**不适合随代码公开分发**，原因有三类：

| 原因 | 涉及数据 | 说明 |
|---|---|---|
| 体积 | 网约车行程、地震目录 | 动辄数百 MB，超出 GitHub 单文件 100 MB 限制 |
| 版权 | 王者荣耀皮肤图、携程/当当页面内容 | 版权不归作者，二次分发有风险 |
| 隐私 | 评教明细、课程评论、17K/裁判文书网账号 | 含可识别个人的信息或登录凭据 |

因此本仓库采用「**代码全量 + 数据分层获取**」的做法：数据要么给出可复现的获取路径，
要么用结构一致的合成数据替代。下面分三层说明。

---

## 第一层：随仓库提供的真实数据

体积小、可公开的样本已直接入库，克隆即可用：

| 位置 | 内容 | 来源 |
|---|---|---|
| `01_coursework/data-analysis-practice/classwork_01_maoyan_top100/*.csv` | 猫眼 Top100 电影、评分分布、时间线 | 课程实训期间爬取并整理 |
| `01_coursework/data-analysis-practice/classwork_02_weibo_hotsearch/*.csv` | 微博热搜热度分级统计 | 同上 |
| `01_coursework/data-analysis-practice/classwork_03_dangdang/*.csv` | 当当图书年度出版量 | 同上 |
| `01_coursework/data-analysis-practice/day01|day02/北京新发地.csv` | 农产品批发价格 | 公开网站整理 |
| `01_coursework/data-analysis-practice/day03/豆瓣250.csv` | 豆瓣 Top250 片单 | 公开榜单整理 |
| `01_coursework/data-analysis-practice/day07/2020-2022疫情数据.xlsx` | 疫情统计数据 | 公开通报汇总 |
| `01_coursework/machine-learning/factor_returns.csv`、`dating.txt` | 多因子收益、约会配对样本 | 课程讲义附带 |
| `01_coursework/text-mining/《人工智能导论》评论（作业）.xls` | 课程评论文本 | 课程作业用样本（已匿名） |
| `01_coursework/text-mining/停用词.txt` | 中文停用词表 | 通用资源 |
| `03_research/provincial-tourism-lda/*_tourism_dict*.txt` | 六省旅游政策自定义词典 | 作者自建 |
| `03_research/provincial-tourism-lda/*_segmented_words*.txt` | 分词结果 | 运行产物，可直接复用 |

---

## 第二层：需自行获取（公开可得）

下面这些数据有合法、可重复的获取路径，仓库只给脚本不给数据：

| 数据 | 获取方式 | 备注 |
|---|---|---|
| 王者荣耀英雄皮肤图 | 运行 `01_coursework/data-analysis-practice/day03/01-王者荣耀.py` | 脚本从官网 CDN 抓取，输出到当前目录；**图片版权归腾讯，请勿再分发** |
| 猫眼 / 豆瓣 / 当当榜单 | 同目录下的爬虫脚本，或改用公开数据集 | 站点改版后选择器可能失效，需自行调整 |
| 微博热搜 | 无公开 API，需自采；也可用公开历史存档 | 注意频控，勿高频请求 |
| 网约车行程 | 原始数据为课程提供；替代方案见下方 `simulate` | 结构：`start_time` 时间戳 |
| 中国地震目录 | 中国地震台网 <https://www.ceic.ac.cn/> 或 USGS <https://earthquake.usgs.gov/fdsnws/event/1/> | USGS 提供 CSV/GeoJSON 接口，字段可直接映射 |
| sklearn 示例集 | `load_iris` / `load_breast_cancer` / `fetch_california_housing` | 代码内直接下载，无需手工准备 |
| Titanic / Instacart / Multi30k | Kaggle、Instacart 官网、Multi30k 官方仓库 | `02_practice/jupyter-notebooks` 用到的公开数据集 |
| bert-base-chinese | HuggingFace `bert-base-chinese`，用 `BERT_MODEL_DIR` 指向本地目录 | 国内可用 ModelScope 镜像 |
| 旅游政策原文（六省细则） | 各省文旅厅官网公开文件 | 放到 `03_research/provincial-tourism-lda/docs/`，或设 `LUO_SOURCE_DIR` |
| 评教明细、课程评论 | **不对外提供** | 含学生/教师个人信息，仅原作者可申请使用 |
| 17K / 裁判文书网账号 | 自行注册，凭据走环境变量 | 见下方「凭据配置」 |

### 凭据配置

爬虫脚本中的手机号、密码、Cookie 已全部移除，改为环境变量：

```bash
export SITE_LOGIN_NAME="你的账号"
export SITE_LOGIN_PWD="你的密码"
export SITE_COOKIE="从浏览器复制的 Cookie"
export ZHIPUAI_API_KEY="你的智谱 Key"     # 方面级情感分析用
```

> 请勿把真实凭据写回代码或提交到仓库。

---

## 第三层：合成数据（零数据也能跑通）

`tools/simulate_data.py` 按各脚本**实际读取的列名与类型**生成结构一致、内容虚构的
数据，随机种子固定，可完全复现。

```bash
# 查看能生成哪些数据集
python tools/simulate_data.py --list

# 全部生成（默认写入各项目自己的 data/ 目录）
python tools/simulate_data.py --dataset all

# 只生成一份，并调整规模与随机种子
python tools/simulate_data.py --dataset trips --rows 50000 --seed 7

# 覆盖已有文件
python tools/simulate_data.py --dataset all --force
```

| 数据集 | 生成文件 | 服务脚本 | 字段 |
|---|---|---|---|
| `finance` | `data-warehouse/data/金融产品购买数据.xlsx` | `work01_01.py` | 购买产品（套餐组合） |
| `tcm` | `data-warehouse/data/中医辨证.xlsx` | `work01_02.py` | 病人症状（按证型成组） |
| `income` | `data-warehouse/data/行业收入表-餐饮服务.xlsx` | `work02_01.py` | 工龄、薪水 |
| `customer` | `data-warehouse/data/客户价值数据表.xlsx` | `work02_02.py` | 历史贷款金额、贷款次数、学历、月收入、性别、客户价值 |
| `credit` | `data-warehouse/data/信用卡精准营销模型.xlsx` | `work03_01.py` | 年龄、月收入、月消费额、持卡数、性别、响应 |
| `trips` | `visualization/data/train_new2.csv` | `new.py` | order_id、start_time、distance_km |
| `quake` | `visualization/data/中国地震数据（2012-2024）_ppman.xlsx` | `zhengli.py` | 发震时刻、经纬度、深度、震级 |
| `reviews` | `course-review-topic-modeling/data/管理类课程评论.xlsx` | `preprocess_comments.py` | 评论 |
| `teaching` | `teaching-reform-analysis/data/2021-2022-2评教统计明细.csv` | `teacher_review_analysis.py` | 姓名、总分、院系、12 个题项（无表头，gbk） |
| `policy` | `provincial-tourism-lda/四川天府旅游命名县（2021年修订）.docx` | `sichuan.py` 等 | 政策条文段落 |

### 生成器的两个设计约束（踩过的坑）

1. **关联规则类数据必须成组出现**。`work01_01/01_02` 的 `min_support` 从 0.05 起，
   完全随机的商品/症状搭配会让所有两两共现低于阈值，频繁项集为空、挖不出任何规则。
   因此生成器按「套餐」「证型」成组采样。
2. **LDA 的文本要覆盖自定义词典**。`provincial-tourism-lda` 只保留词典词与白名单词，
   自由造句会导致词表过小、模型退化。生成器直接读取同目录的 `*_tourism_dict*.txt`
   作为词源造句。

合成数据的生成文件已在 `.gitignore` 中忽略，属于「本地才需要」的内容。

---

## 大数据集怎么分发（本仓库没用上的方案）

如果确实需要把大文件公开给别人，按推荐顺序：

| 方案 | 适用 | 成本 |
|---|---|---|
| **GitHub Releases 附件** | 单个打包文件 < 2 GB，无需版本控制 | 免费，一条 `gh release upload` 即可 |
| **Git LFS** | 需按版本管理的大文件 | 免费额度 1 GB 存储 + 1 GB/月流量，超出收费 |
| **HuggingFace Datasets** | 数据集本身有复用价值 | 免费公开，自带在线浏览与 `datasets.load_dataset()` |
| **Zenodo / 图床网盘** | 需要 DOI、长期归档 | 免费，适合论文配套数据 |
| **只给获取脚本** | 数据可重新抓取，或版权不归自己 | 零成本，也是本仓库的选择 |

本仓库数据总量不大，但都属「可重新生成」或「不可再分发」，因此选择最后一档：
**给脚本 + 给合成器，不给二进制数据**。

---

## 合规提醒

- 爬虫脚本仅供学习，请遵守目标站点的 `robots.txt` 与服务条款，控制请求频率。
- 涉及个人信息的评教、评论数据未入库，请勿尝试从其他渠道获取他人数据。
- 合成数据不含任何真实个人信息，可自由使用。
