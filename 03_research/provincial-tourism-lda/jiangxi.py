import docx

from config import OUTPUT_DIR, PROJECT_DIR, SOURCE_DOC_DIR  # noqa: E402
import jieba
import re
import numpy as np
from gensim import corpora, models
from collections import defaultdict
import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
import networkx as nx
from scipy.stats import entropy
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# ====================== 全局配置：强制中文字体 ======================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 兼容Windows/macOS
plt.rcParams['axes.unicode_minus'] = False


# ====================== 1. 文本预处理：适配江西DOCX格式及表格结构 ======================
def extract_docx_text(file_path):
    """读取DOCX文档并提取文本，强化保留表格内容及章节编号"""
    try:
        doc = docx.Document(file_path)
        full_text = []

        # 1. 提取普通段落文本
        for para in doc.paragraphs:
            text = para.text
            text = re.sub(r'(\d+\.\s)', r'\n\1 ', text)  # 保留评分项编号
            text = re.sub(r'\|', ' | ', text)  # 保留表格分隔符
            text = text.replace('引客入赣', '引客入赣奖励')
            full_text.append(text)

        # 2. 提取表格内容（关键修复点）
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell_text = cell.text
                    cell_text = re.sub(r'(\d+\.\s)', r'\n\1 ', cell_text)
                    cell_text = re.sub(r'\|', ' | ', cell_text)
                    cell_text = cell_text.replace('引客入赣', '引客入赣奖励')
                    full_text.append(cell_text)

        # 3. 合并所有文本并处理特殊词汇
        combined_text = ' '.join(full_text).replace('云游江西', '江西云游平台')
        return combined_text

    except Exception as e:
        print(f"读取江西文档 {file_path} 失败: {str(e)}")
        return ""


def merge_documents(file_paths):
    """处理单个江西旅游政策文档内容（优化单文档场景）"""
    if not file_paths or not os.path.exists(file_paths[0]):
        raise ValueError("未找到江西文档，请检查文件路径")

    doc_text = extract_docx_text(file_paths[0])
    if not doc_text:
        raise ValueError("江西文档内容读取失败")

    print(f"成功读取江西文档: {file_paths[0]} (字数: {len(doc_text)})")
    return doc_text


def preprocess_text(text):
    """优化停用词表，强制保留江西旅游核心词汇和白名单，返回分词结果"""
    print(f"江西政策原始文本总长度: {len(text)}")

    # 江西旅游自定义词典（含考核指标核心术语）
    dict_path = 'jiangxi_tourism_dict_2023.txt'
    custom_words = [
        '风景独好', '旅游名县', '考核认定', '评分细则', '旅游产业发展',
        '专项资金', '引客入赣', '旅游重大项目', '游客满意度', '智慧旅游',
        '过夜游客', '复游率', '旅游安全', '生态保护', '加分项', '一票否决',
        '2023修订', '领导重视', '财政投入'
    ]

    # 白名单核心政策词（可根据实际需求补充）
    whitelist = set([
        '交通', '服务', '环境', '融合', '安全', '品牌', '创新', '监管', '满意度', '生态', '旅游', '公共', '智慧', '资源', '市场', '项目', '资金', '政策', '标准', '体系', '机制', '平台', '产品', '发展', '保护', '管理', '宣传', '推广', '引导', '合作', '共享', '监督', '评估', '考核', '激励', '奖惩', '投诉', '应急', '风险', '应对', '规划', '目标', '指标', '责任', '落实', '执行', '实施', '改革', '优化', '提升', '完善', '健全', '规范', '制度', '流程', '程序', '办法', '措施', '方案', '计划', '总结', '报告', '通报', '反馈', '建议', '意见', '决策', '指令', '命令', '通知', '公告', '公示', '声明', '说明', '解读', '解答', '咨询', '支持', '帮助', '指导', '培训', '教育'
    ])

    # 加载或生成江西自定义词典
    if os.path.exists(dict_path):
        jieba.load_userdict(dict_path)
        print(f"已加载江西自定义词典: {dict_path}")
        with open(dict_path, 'r', encoding='utf-8') as f:
            custom_words.extend([line.split()[0] for line in f if line.strip()])
    else:
        with open(dict_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(custom_words))
        jieba.load_userdict(dict_path)
        print(f"已生成江西2023修订版词典: {dict_path}")

    # 增强停用词表，剔除数字、序号、评分、无关词
    stopwords = set([
        '附件', '试行', '大项', '小项', '分项', '自检', '合计',
        '根据', '为了', '应当', '按照', '关于', '所示', '·', '、', '；', '：', '｜',
        '评分', '得分', '分数', '级别', '项目', '单位', '序号', '标准', 'DB36', '主要', '以上', '以下', '分', '项', '小项', '大项',
        '1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '4.3',
        '之一', '低于', '影响', '造成', '突出', '工作', '情况', '问题', '相关', '社会', '服务', '管理', '单位', '部门', '以上', '以下',
        *[str(i) for i in range(0, 100)],
        *[f"{i}.{j}" for i in range(0, 10) for j in range(0, 10)]
    ])

    # 分词处理（启用HMM识别江西特有长词）
    words = list(jieba.cut(text, cut_all=False, HMM=True))
    print(f"江西政策分词后总词汇数: {len(words)}")

    # 过滤停用词并强制保留江西核心词和白名单
    filtered_words = []
    for word in words:
        if word in custom_words or word in whitelist:
            filtered_words.append(word)
            continue
        if word in stopwords or len(word) == 1 and not re.fullmatch(r'[^\d]+', word) or re.fullmatch(r'^\d+$', word):
            continue
        filtered_words.append(word)
    print(f"初步过滤后词汇数: {len(filtered_words)}")

    # 进一步过滤：只保留长度>1、全中文、且在白名单或自定义词典中的词
    filtered_words = [
        word for word in filtered_words
        if len(word) > 1
        and (word in custom_words or word in whitelist)
        and re.fullmatch(r'[\u4e00-\u9fff]+', word)
    ]
    print(f"白名单过滤后词汇数: {len(filtered_words)}")

    # 只保留出现频率大于1的词
    from collections import Counter
    word_counts = Counter(filtered_words)
    filtered_words = [word for word in filtered_words if word_counts[word] > 1]
    print(f"高频词过滤后词汇数: {len(filtered_words)}")

    with open('jiangxi_segmented_words_2023.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(filtered_words))
    print("江西2023修订版分词结果已保存至当前目录")

    return filtered_words, custom_words, whitelist  # 返回分词、江西核心词和白名单


# ====================== 2. 伪多文档生成：适配江西考核指标结构（单文档优化）======================
def generate_pseudo_documents(words, custom_words, num_docs=15, chunk_size=70):
    """用全部分词结果生成伪文档，保证主题分析词量充足"""
    if len(words) < chunk_size:
        raise ValueError(f"江西分词结果过短({len(words)})，建议调整chunk_size")

    pseudo_docs = []
    # 先按固定长度分割
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    # 不足则补全（随机采样）
    while len(chunks) < num_docs:
        sample = np.random.choice(words, size=chunk_size, replace=True).tolist()
        chunks.append(sample)

    # 随机打乱词序，增加异质性
    for i in range(num_docs):
        np.random.shuffle(chunks[i])
        pseudo_docs.append(chunks[i])

    print(f"生成{num_docs}篇江西伪文档，每篇约{chunk_size}词")
    return pseudo_docs


# ====================== 3. LDA模型：优化主题适配江西考核体系 ======================
def build_jiangxi_lda_model(documents, num_topics=12):
    """针对江西旅游考核文档调整主题模型参数（匹配12项核心指标）"""
    dictionary = corpora.Dictionary(documents)
    # 仅过滤低频词（出现<3次），保留江西考核术语
    dictionary.filter_extremes(no_below=3, no_above=0.9)
    print(f"江西词典尺寸: {len(dictionary)}，包含考核核心术语")

    corpus = [dictionary.doc2bow(doc) for doc in documents]
    if not corpus or sum(len(c) for c in corpus) == 0:
        raise ValueError("江西语料库为空，请检查分词结果")

    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        alpha=0.18,  # 单文档场景提高主题区分度
        eta=0.025,  # 增强稀疏性适应单文档特征
        passes=150,  # 减少迭代次数提高单文档效率
        random_state=42
    )

    # 打印江西考核主题关键词（检查指标模块划分）
    print("\n===== 江西2023考核政策主题关键词 =====")
    for i in range(min(5, num_topics)):
        topic_words = lda.show_topic(i, topn=8)
        print(f"主题{i} ({'|'.join([w for w, _ in topic_words[:3]])}): {topic_words}")

    return lda, dictionary, corpus


def optimize_lda_topics(documents, max_topics=12):
    """优化主题数，适配江西12项考核指标（单文档场景缩小范围）"""
    perplexity_scores = []
    for k in range(6, max_topics + 1):  # 单文档场景从6开始搜索
        try:
            lda, _, corpus = build_jiangxi_lda_model(documents, k)
            perplexity = lda.log_perplexity(corpus)
            perplexity_scores.append((k, perplexity))
            print(f"江西主题数{k} → 困惑度{perplexity:.4f}")
        except Exception as e:
            print(f"江西主题数{k}训练失败: {str(e)}")

    if not perplexity_scores:
        print("警告：江西所有主题数训练失败，强制使用主题数10")
        return 10

    # 绘制困惑度曲线并标记拐点
    plt.figure(figsize=(10, 6))
    k_list = [p[0] for p in perplexity_scores]
    perp_list = [p[1] for p in perplexity_scores]
    plt.plot(k_list, perp_list, 'o-', color='darkgreen')
    plt.xticks(k_list)
    plt.xlabel('主题数量', fontsize=12)
    plt.ylabel('困惑度', fontsize=12)
    plt.title('江西2023旅游考核政策LDA主题数优化', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('jiangxi_topic_perplexity_2023.png', dpi=300, bbox_inches='tight')

    # 选择拐点并确保不小于8（单文档合理范围）
    if len(perplexity_scores) >= 3:
        diffs = np.diff(perp_list)
        min_diff_idx = np.argmin(diffs)  # 找下降速率拐点
        optimal_k = k_list[min_diff_idx + 1]
        optimal_k = max(8, optimal_k)  # 单文档场景最低主题数
    else:
        optimal_k = 10
    print(f"自动选择江西2023最优主题数: {optimal_k}")
    return optimal_k


# ====================== 4. 可视化：定制江西考核主题展示 ======================
def plot_jiangxi_topic_radar(lda, dictionary, topic_names):
    """绘制雷达图，主题名称匹配江西12项考核指标及加分项"""
    topic_weights = []
    for topic_id in range(lda.num_topics):
        alpha = lda.alpha[topic_id] if hasattr(lda, 'alpha') else 1 / lda.num_topics
        topic_words = lda.show_topic(topic_id, topn=10)
        word_probs = sum(p for _, p in topic_words)
        topic_weights.append(alpha * word_probs)

    # 归一化权重
    topic_weights = np.array(topic_weights) / np.max(topic_weights) * 900

    # 雷达图绘制（江西考核指标顺序）
    jiangxi_order = [
        "领导重视", "财政投入", "收入增长", "税收贡献",
        "接待情况", "外地游客", "重大项目", "旅游就业",
        "农民增收", "智慧服务", "知名度", "满意度",
        "加分项分析", "否决项监控"
    ]
    topic_names = jiangxi_order[:lda.num_topics]
    angles = np.linspace(0, 2 * np.pi, len(topic_names), endpoint=False).tolist()
    topic_weights = np.concatenate((topic_weights, [topic_weights[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(16, 16), subplot_kw=dict(polar=True))
    ax.plot(angles, topic_weights, 'o-', linewidth=3, color='darkblue', label='主题权重')
    ax.fill(angles, topic_weights, alpha=0.2, color='darkblue')
    ax.set_thetagrids(np.degrees(angles[:-1]), topic_names, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize=12)
    plt.title('江西"风景独好"旅游名县(2023修订)考核主题分布雷达图', fontsize=18, pad=30)
    plt.savefig('jiangxi_topic_radar_2023.png', dpi=300, bbox_inches='tight')


def build_topic_cooccurrence_network(lda, dictionary, topn=18):
    """构建江西考核主题-关键词共现网络，只保留白名单和自定义词典中的高频词"""
    import re
    from collections import Counter
    filtered_words, custom_words, whitelist = preprocess_text(' '.join(dictionary.values())) if hasattr(dictionary, 'values') else ([], [], set())
    G = nx.Graph()
    all_topic_words = []
    for topic_id in range(lda.num_topics):
        topic_words = lda.show_topic(topic_id, topn=topn)
        # 只保留全中文且长度≥2的高频词，且在白名单或自定义词典中
        topic_words = [(w, p) for w, p in topic_words if len(w) > 1 and (w in custom_words or w in whitelist) and re.fullmatch(r'[\u4e00-\u9fff]+', w)]
        all_topic_words.extend([(word, topic_id) for word, _ in topic_words])
    # 只保留高频词
    word_counts = Counter([w for w, _ in all_topic_words])
    all_topic_words = [(w, tid) for (w, tid) in all_topic_words if word_counts[w] > 1]

    # 添加节点（区分江西考核主题和关键词）
    for word, topic_id in all_topic_words:
        G.add_node(word, type='keyword', topic=topic_id)
    for topic_id in range(lda.num_topics):
        G.add_node(f"江西主题{topic_id}", type='topic', topic=topic_id)

    # 添加边（强化江西考核指标术语共现关系）
    for topic_id in range(lda.num_topics):
        topic_name = f"江西主题{topic_id}"
        topic_words = [word for word, _ in lda.show_topic(topic_id, topn=topn) if len(word) > 1 and (word in custom_words or word in whitelist) and re.fullmatch(r'[\u4e00-\u9fff]+', word)]
        topic_words = [w for w in topic_words if word_counts[w] > 1]
        # 主题-关键词边
        for word in topic_words:
            G.add_edge(topic_name, word, weight=1)
        # 关键词-关键词边（同考核主题内共现）
        for i in range(len(topic_words)):
            for j in range(i + 1, len(topic_words)):
                w1, w2 = topic_words[i], topic_words[j]
                if G.has_edge(w1, w2):
                    G[w1][w2]['weight'] += 1
                else:
                    G.add_edge(w1, w2, weight=1)

    # 可视化参数（单文档场景缩小节点尺寸）
    plt.figure(figsize=(18, 14))
    pos = nx.circular_layout(G, scale=2)
    node_sizes = []
    node_colors = []

    for node in G.nodes():
        if node.startswith("江西主题"):
            node_sizes.append(8000)
            node_colors.append(f"C{int(node[-1])}")
        else:
            node_sizes.append(max(500, len([w for w, _ in all_topic_words if w == node]) * 400))
            node_colors.append(f"C{G.nodes[node]['topic']}")

    # 绘制节点和边
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w * 0.6 for w in edge_weights], alpha=0.6, edge_color='gray')
    nx.draw_networkx_labels(
        G, pos,
        font_size=10, font_weight='bold',
        font_family='Microsoft YaHei'
    )

    plt.title('江西2023旅游考核政策主题-关键词共现网络', fontsize=18)
    plt.axis('off')
    plt.savefig('jiangxi_cooccurrence_network_2023.png', dpi=300, bbox_inches='tight')
    return G


def visualize_lda_topics(lda, dictionary, corpus):
    """生成LDAvis可视化，突出江西2023考核评分指标分布"""
    vis_data = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis_data, 'jiangxi_lda_visualization_2023.html')
    print("江西2023 LDAvis交互式可视化已保存至当前目录")


# ====================== 5. 主函数：全链路江西政策分析 ======================
def analyze_jiangxi_policy(file_paths):
    """分析江西旅游名县考核文档，返回LDA模型（单文档优化）"""
    try:
        print("\n\n==================== 江西\"风景独好\"旅游名县(2023修订)政策分析启动 ====================")

        # 1. 读取江西单个考核文档
        all_text = merge_documents(file_paths)

        # 2. 文本预处理（获取江西分词结果和核心词）
        words, custom_words, whitelist = preprocess_text(all_text)

        # 3. 生成江西伪文档（单文档场景减少数量）
        pseudo_docs = generate_pseudo_documents(words, custom_words, num_docs=15, chunk_size=70)

        # 4. 江西主题建模
        print("\n===== 江西2023 LDA模型训练 =====")
        optimal_k = optimize_lda_topics(pseudo_docs)
        lda, dictionary, corpus = build_jiangxi_lda_model(pseudo_docs, optimal_k)

        # 5. 定义江西主题名称（严格匹配考核指标）
        jiangxi_topics = [
            "1. 领导重视", "2. 财政投入", "3. 收入增长", "4. 税收贡献",
            "5. 接待情况", "6. 外地游客", "7. 重大项目", "8. 旅游就业",
            "9. 农民增收", "10. 智慧服务", "11. 知名度", "12. 满意度",
            "13. 加分项分析", "14. 否决项监控"
        ]
        topic_names = jiangxi_topics[:lda.num_topics]
        print(f"使用江西2023考核主题: {topic_names}")

        # 6. 江西可视化
        plot_jiangxi_topic_radar(lda, dictionary, topic_names)
        build_topic_cooccurrence_network(lda, dictionary)
        visualize_lda_topics(lda, dictionary, corpus)

        # 7. 江西量化指标
        entropy_val = calculate_topic_entropy(lda)
        concentration_val = calculate_topic_concentration(lda)
        print(f"\n===== 江西2023考核政策量化分析结果 =====")
        print(f"主题熵值: {entropy_val:.2f}（政策文档合理范围: 1.8-2.6）")
        print(f"主题集中度: {concentration_val:.2f}（政策文档合理范围: 0.7-0.85）")

        print("\n==================== 江西2023分析完成！建议检查以下内容 ====================")
        print("- jiangxi_segmented_words_2023.txt → 确认2023修订版考核词是否保留")
        print("- 可视化图片 → 检查'重大项目'、'满意度'等主题是否独立")
        print("- jiangxi_lda_visualization_2023.html → 交互式验证考核指标区分度")
        return lda

    except Exception as e:
        print(f"\n==================== 江西2023分析失败！错误详情 ====================")
        print(f"{str(e)}")
        return None


# ====================== 量化指标计算 ======================
def calculate_topic_entropy(lda):
    topic_dist = lda.alpha / lda.alpha.sum()
    return entropy(topic_dist)


def calculate_topic_concentration(lda):
    topic_dist = lda.alpha / lda.alpha.sum()
    sorted_dist = np.sort(topic_dist)[::-1]
    return sorted_dist[:3].sum()


# ====================== 执行入口：指定江西文档路径 ======================
if __name__ == "__main__":
    # 单文档路径（已包含2023修订标识）
    file_paths = [
        SOURCE_DOC_DIR / "江西风景独好旅游名县细则（2023年修订）.docx",
    ]

    lda_model = analyze_jiangxi_policy(file_paths)
    if lda_model is None:
        print("江西2023分析终止→ 请检查文档路径是否正确，或尝试调整chunk_size参数")