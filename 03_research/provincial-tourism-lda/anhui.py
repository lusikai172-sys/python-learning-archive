import PyPDF2

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
import pdfplumber

# ====================== 全局配置：强制中文字体 ======================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 兼容Windows/macOS
plt.rcParams['axes.unicode_minus'] = False


# ====================== 1. 文本预处理：确保核心词保留 ======================
def extract_anhui_text(file_path):
    """使用pdfplumber提取PDF全部文本，兼容性更好"""
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ''
            text += page_text
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    return text


def preprocess_text(text):
    """深度优化预处理，精准过滤无关词，确保核心政策词留存"""
    print(f"原始文本长度: {len(text)}")

    # 自定义词典（优化加载逻辑，增加友好提示）
    dict_path = PROJECT_DIR / 'anhui_tourism_dict.txt'
    if os.path.exists(dict_path):
        jieba.load_userdict(dict_path)
        print(f"自定义词典加载成功: {dict_path}")
        with open(dict_path, 'r', encoding='utf-8') as f:
            custom_words = [line.split()[0] for line in f if line.strip()]
        print(f"词典核心词示例: {custom_words[:10]}（若核心词未加载全，检查词典格式）")
    else:
        print("警告：自定义词典不存在！！！建议补充政策核心词（如安徽省县域旅游、政策细则等）词典，否则可能影响分词！")
        custom_words = []

    # 增强停用词表，剔除数字、序号、评分等无关词
    stopwords = set([
        '附录', '规范性', '管理局', '大项', '小项', '分项',
        '自检', '合计', '根据', '为了', '应当', '按照',
        '关于', '所示', '（', '）', '【', '】', '·', '、', '；', '：',
        '评分', '得分', '分数', '级别', '项目', '单位', '序号', '标准', 'DB34', '主要', '以上', '以下', '分', '项', '小项', '大项',
        '1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '4.3',
        # 过滤所有数字和小数
        *[str(i) for i in range(0, 100)],
        *[f"{i}.{j}" for i in range(0, 10) for j in range(0, 10)]
    ])

    # 分词（强制启用HMM提高长词识别，适配政策长术语）
    words = list(jieba.cut(text, cut_all=False, HMM=True))
    print(f"分词后词汇数: {len(words)}")

    # 过滤停用词（核心词强制保留+精准过滤无关词）
    filtered_words = []
    for word in words:
        # 优先保留自定义词典核心词
        if word in custom_words:
            filtered_words.append(word)
            continue
        # 过滤停用词、单字（除可能的政策特殊单字，如"皖"等，这里假设无，可根据实际补充）、纯数字
        if word in stopwords or len(word) == 1 and not re.fullmatch(r'[^\d]+', word) or re.fullmatch(r'^\d+$', word):
            continue
        filtered_words.append(word)
    print(f"初步过滤后词汇数: {len(filtered_words)}")

    # 进一步过滤仅为数字、序号、评分等无关词
    filtered_words = [
        word for word in filtered_words
        if not re.fullmatch(r'\d+(\.\d+)?', word)  # 纯数字/小数
        and word not in stopwords
        and len(word) > 1
    ]
    print(f"严格过滤后词汇数: {len(filtered_words)}")

    # 保存分词结果（必看！检查是否丢失核心词）
    with open('anhui_segmented_words.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(filtered_words))
    print("分词结果已保存至anhui_segmented_words.txt → 必须手动检查核心词（如安徽省县域旅游、政策细则等）是否存在！")

    return filtered_words


# ====================== 2. 伪多文档生成：模拟真实多文档 ======================
def generate_pseudo_documents(words, num_docs=15, chunk_size=50):
    """
    用全部分词结果生成伪文档，保证主题分析词量充足
    - chunk_size: 每篇伪文档的词汇量（模拟真实文档长度）
    - num_docs: 伪文档数量
    """
    filtered_words = words  # 直接用全部分词结果

    if len(filtered_words) < chunk_size:
        raise ValueError("分词结果过短，无法生成有效伪文档")

    pseudo_documents = []
    # 先按固定长度分割
    chunks = [filtered_words[i:i + chunk_size] for i in range(0, len(filtered_words), chunk_size)]
    # 不足则补全（随机采样）
    while len(chunks) < num_docs:
        sample = np.random.choice(filtered_words, size=chunk_size, replace=True).tolist()
        chunks.append(sample)

    # 随机打乱词序，增加异质性
    for i in range(num_docs):
        np.random.shuffle(chunks[i])
        pseudo_documents.append(chunks[i])

    print(f"生成{num_docs}篇伪文档，每篇约{chunk_size}词")
    return pseudo_documents


# ====================== 3. LDA模型：强制主题区分 ======================
def build_anhui_lda_model(documents, num_topics=6):
    """
    手动设置超参数，强制主题稀疏：
    - alpha=0.1: 文档-主题分布更集中
    - eta=0.01: 主题-词分布更稀疏
    - passes=150: 确保收敛
    """
    dictionary = corpora.Dictionary(documents)
    # 仅过滤极端低频词（出现次数<3），保留政策核心词
    dictionary.filter_extremes(no_below=3, no_above=0.9)  # 修复过度过滤
    print(f"词典尺寸: {len(dictionary)} → 必须包含核心政策词（如文化旅游名县）")

    corpus = [dictionary.doc2bow(doc) for doc in documents]
    if not any(corpus):
        raise ValueError("语料库为空！检查分词结果")

    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        alpha=0.1,  # 手动控制主题集中度
        eta=0.01,  # 手动控制词分布稀疏度
        passes=150,  # 增加迭代确保收敛
        random_state=42
    )

    # 打印前3个主题的关键词（必看！检查是否合理）
    for i in range(min(3, num_topics)):
        print(f"主题{i}关键词: {lda.show_topic(i, topn=10)}")

    return lda, dictionary, corpus


def optimize_lda_topics(documents, max_topics=8):
    """修复困惑度计算，强制输出有效主题"""
    perplexity_scores = []
    for k in range(3, max_topics + 1):
        try:
            lda, _, corpus = build_anhui_lda_model(documents, k)
            perplexity = lda.log_perplexity(corpus)
            perplexity_scores.append((k, perplexity))
            print(f"主题数{k} → 困惑度{perplexity:.4f}")
        except Exception as e:
            print(f"主题数{k}失败: {str(e)}")

    if not perplexity_scores:
        print("警告：所有主题数均失败！强制使用主题数6")
        return 6

    # 绘制困惑度曲线（强制标记坐标）
    plt.figure(figsize=(10, 6))
    k_list = [p[0] for p in perplexity_scores]
    perp_list = [p[1] for p in perplexity_scores]
    plt.plot(k_list, perp_list, 'o-', color='crimson')
    plt.xticks(k_list)  # 强制显示所有尝试的主题数
    plt.xlabel('主题数量', fontsize=12)
    plt.ylabel('困惑度', fontsize=12)
    plt.title('安徽文化旅游政策LDA主题数优化', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('anhui_topic_perplexity.png', dpi=300, bbox_inches='tight')

    # 选拐点（下降变缓时的主题数）
    diffs = np.diff(perp_list)
    min_diff_idx = np.argmin(diffs)  # 找下降最快后的拐点
    optimal_k = k_list[min_diff_idx + 1]
    print(f"自动选择最优主题数: {optimal_k}（基于困惑度变化率）")
    return optimal_k


# ====================== 4. 可视化：重构逻辑，确保效果 ======================
def plot_anhui_topic_radar(lda, dictionary, topic_names):
    """
    重构权重计算：直接使用主题的总概率（alpha）+ 关键词匹配度
    """
    topic_weights = []
    for topic_id in range(lda.num_topics):
        # 主题的先验权重（alpha）
        alpha = lda.alpha[topic_id] if hasattr(lda, 'alpha') else 1 / lda.num_topics
        # 关键词与主题的匹配度（取前10个词的概率和）
        topic_words = lda.show_topic(topic_id, topn=10)
        word_probs = sum(p for _, p in topic_words)
        topic_weights.append(alpha * word_probs)

    # 归一化权重（确保雷达图维度均衡）
    topic_weights = np.array(topic_weights) / np.max(topic_weights) * 1000  # 缩放至合理范围

    # 雷达图绘制
    angles = np.linspace(0, 2 * np.pi, len(topic_names), endpoint=False).tolist()
    topic_weights = np.concatenate((topic_weights, [topic_weights[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
    ax.plot(angles, topic_weights, 'o-', linewidth=2, color='darkcyan', label='主题权重')
    ax.fill(angles, topic_weights, alpha=0.2, color='darkcyan')
    ax.set_thetagrids(np.degrees(angles[:-1]), topic_names, fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7, color='gray')
    ax.legend(loc='upper right', fontsize=12)
    plt.title('安徽文化旅游政策主题分布雷达图', fontsize=16, pad=20)
    plt.savefig('anhui_topic_radar.png', dpi=300, bbox_inches='tight')


def build_topic_cooccurrence_network(lda, dictionary, topn=20):
    """
    重构共现网络：
    - 每个主题取20个关键词（确保节点充足）
    - 使用circular布局（避免节点重叠）
    - 节点大小按词频，颜色区分主题/关键词
    """
    G = nx.Graph()
    # 先收集所有主题的关键词
    all_topic_words = []
    for topic_id in range(lda.num_topics):
        topic_words = lda.show_topic(topic_id, topn=topn)
        all_topic_words.extend([(word, topic_id) for word, _ in topic_words])

    # 添加节点（区分主题和关键词）
    for word, topic_id in all_topic_words:
        G.add_node(word, type='keyword', topic=topic_id)
    for topic_id in range(lda.num_topics):
        G.add_node(f"主题{topic_id}", type='topic', topic=topic_id)

    # 添加边（主题→关键词，关键词→关键词）
    for topic_id in range(lda.num_topics):
        topic_name = f"主题{topic_id}"
        topic_words = [word for word, _ in lda.show_topic(topic_id, topn=topn)]
        # 主题→关键词
        for word in topic_words:
            G.add_edge(topic_name, word, weight=1)
        # 关键词→关键词（同主题内共现）
        for i in range(len(topic_words)):
            for j in range(i + 1, len(topic_words)):
                w1, w2 = topic_words[i], topic_words[j]
                if G.has_edge(w1, w2):
                    G[w1][w2]['weight'] += 1
                else:
                    G.add_edge(w1, w2, weight=1)

    # 可视化参数
    plt.figure(figsize=(16, 12))
    # 布局：circular更稳定
    pos = nx.circular_layout(G, scale=1.5)  # 扩大布局范围
    # 节点大小：主题节点固定6000，关键词按词频
    node_sizes = []
    node_colors = []
    for node in G.nodes():
        if node.startswith("主题"):
            node_sizes.append(6000)
            node_colors.append(f"C{int(node[-1])}")  # 主题颜色区分
        else:
            # 关键词大小按出现次数（在多少主题中出现）
            count = sum(1 for _, tid in all_topic_words if _ == node)
            node_sizes.append(max(500, count * 500))
            node_colors.append(f"C{G.nodes[node]['topic']}")  # 同主题同色

    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    # 绘制边（按权重调整宽度）
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w * 0.5 for w in edge_weights], alpha=0.6, edge_color='gray')
    # 绘制标签（主题标签加大）
    node_labels = {}
    for node in G.nodes():
        if node.startswith("主题"):
            node_labels[node] = node + "\n(主题)"
        else:
            node_labels[node] = node
    nx.draw_networkx_labels(
        G, pos, labels=node_labels,
        font_size=10, font_weight='bold',
        font_family='Microsoft YaHei'
    )

    plt.title('安徽文化旅游政策主题-关键词共现网络', fontsize=16)
    plt.axis('off')
    plt.savefig('anhui_cooccurrence_network.png', dpi=300, bbox_inches='tight')
    return G


def visualize_lda_topics(lda, dictionary, corpus):
    """修复LDAvis配置，强制显示多主题"""
    vis_data = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis_data, 'anhui_lda_visualization.html')
    print("LDAvis已保存 → 浏览器打开后，拖动左侧圆圈查看多主题！")


# ====================== 5. 主函数：全链路管控 ======================
def analyze_anhui_policy(file_path):
    try:
        print("\n\n==================== 安徽文化旅游政策分析启动 ====================")

        # 1. 文本提取（强制检查）
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        text = extract_anhui_text(file_path)
        if len(text) < 1000:
            raise ValueError("文本提取异常（长度<1000）→ 检查PDF是否加密")

        # 2. 预处理（强制人工验证分词结果）
        words = preprocess_text(text)
        if len(words) < 500:
            raise ValueError("分词后词汇数<500 → 检查停用词表或自定义词典")

        # 3. 伪文档生成（强制异质化）
        pseudo_docs = generate_pseudo_documents(words, num_docs=15, chunk_size=80)
        if len(pseudo_docs) < 5:
            raise ValueError("伪文档生成失败→ 检查分词长度")

        # 4. 主题建模（强制输出中间结果）
        print("\n===== LDA模型训练 =====")
        optimal_k = optimize_lda_topics(pseudo_docs)
        lda, dictionary, corpus = build_anhui_lda_model(pseudo_docs, optimal_k)
        if lda.num_topics < 3:
            raise ValueError("LDA仅生成<3个主题→ 检查超参数或伪文档")

        # 5. 可视化：动态匹配主题名称
        base_topic_names = [
            "文化资源保护", "旅游经济发展", "公共服务配套",
            "产业融合创新", "监管与服务质量", "保障机制建设"
        ]
        # 按实际主题数截取/扩展名称
        topic_names = base_topic_names[:lda.num_topics]
        if len(topic_names) < lda.num_topics:
            extra_count = lda.num_topics - len(topic_names)
            for i in range(extra_count):
                topic_names.append(f"拓展主题{i + 1}")
        print(f"使用主题名称: {topic_names}")

        plot_anhui_topic_radar(lda, dictionary, topic_names)
        build_topic_cooccurrence_network(lda, dictionary)
        visualize_lda_topics(lda, dictionary, corpus)

        # 6. 量化指标（验证合理性）
        entropy_val = calculate_topic_entropy(lda)
        concentration_val = calculate_topic_concentration(lda)
        print(f"\n===== 量化指标 =====")
        print(f"主题熵值: {entropy_val:.2f}（1.5-2.5为合理范围）")
        print(f"主题集中度: {concentration_val:.2f}（0.6-0.8为合理范围）")

        print("\n==================== 分析完成！务必检查以下文件 ====================")
        print("- anhui_segmented_words.txt → 确认核心词存在")
        print("- 各可视化图片及HTML → 检查主题区分度")
        return lda

    except Exception as e:
        print(f"\n==================== 分析失败！错误原因 ====================")
        print(f"{str(e)}")
        return None


# ====================== 量化指标（保持不变） ======================
def calculate_topic_entropy(lda):
    topic_dist = lda.alpha / lda.alpha.sum()
    return entropy(topic_dist)


def calculate_topic_concentration(lda):
    topic_dist = lda.alpha / lda.alpha.sum()
    sorted_dist = np.sort(topic_dist)[::-1]
    return sorted_dist[:3].sum()


# ====================== 执行入口：强制报错定位 ======================
if __name__ == "__main__":
    file_path = SOURCE_DOC_DIR / "安徽文化旅游名县(市、区)评定（2019年修订）.pdf"
    lda = analyze_anhui_policy(file_path)
    if lda is None:
        print("强制终止→ 必须修复上述错误后重新运行！")