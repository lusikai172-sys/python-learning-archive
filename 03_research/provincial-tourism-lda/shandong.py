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

# ====================== 全局配置：强制中文字体 ======================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 兼容Windows/macOS
plt.rcParams['axes.unicode_minus'] = False


# ====================== 1. 文本预处理：适配山东PDF格式 ======================
def extract_shandong_text(file_path):
    """从PDF提取山东全域旅游政策文本，保留表格和章节结构"""
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ''
        for page in pdf_reader.pages:
            page_text = page.extract_text() or ''
            # 保留评分表结构（如4.1.1 森林覆盖率高）
            text += re.sub(r'^\s*\|\s*(\d+\.\d+\.\d+)\s*\|\s*([^\|]+)\s*\|\s*(\d+)\s*\|\s*.*$\n',
                           r'\1 \2 \3\n', page_text, flags=re.MULTILINE)
            # 强化章节标题识别
            text = re.sub(r'^(\d+\.\d+)\s+([^\n]+)$', r'\n\1 \2\n', text, flags=re.MULTILINE)
            # 移除页码和重复头部
            text = re.sub(r'(\d+/\d+)|(烟台市文化和旅游局)', '', text)
    return text


def preprocess_text(text):
    """山东政策分词优化，保留评定核心指标和白名单机制"""
    print(f"山东政策原始文本长度: {len(text)}")

    # 山东旅游自定义词典（含核心评定术语）
    dict_path = 'shandong_tourism_dict.txt'
    custom_words = [
        '全域旅游', '评定标准', '城乡环境', '旅游公共服务',
        '旅游发展效益', '综合竞争力', '保障机制', '森林覆盖率',
        '适游天数', '游客满意度', '旅游度假区', '乡村旅游'
    ]

    # 白名单核心政策词（可根据实际需求补充）
    whitelist = set([
        '交通', '服务', '环境', '融合', '安全', '品牌', '创新', '监管', '满意度', '生态', '旅游', '公共', '智慧', '资源', '市场', '项目', '资金', '政策', '标准', '体系', '机制', '平台', '产品', '发展', '保护', '管理', '宣传', '推广', '引导', '合作', '共享', '监督', '评估', '考核', '激励', '奖惩', '投诉', '应急', '风险', '应对', '规划', '目标', '指标', '责任', '落实', '执行', '实施', '改革', '优化', '提升', '完善', '健全', '规范', '制度', '流程', '程序', '办法', '措施', '方案', '计划', '总结', '报告', '通报', '反馈', '建议', '意见', '决策', '指令', '命令', '通知', '公告', '公示', '声明', '说明', '解读', '解答', '咨询', '支持', '帮助', '指导', '培训', '教育'
    ])

    # 加载或生成山东词典
    if os.path.exists(dict_path):
        jieba.load_userdict(dict_path)
        print(f"已加载山东自定义词典: {dict_path}")
        with open(dict_path, 'r', encoding='utf-8') as f:
            custom_words.extend([line.split()[0] for line in f if line.strip()])
    else:
        with open(dict_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(custom_words))
        jieba.load_userdict(dict_path)
        print(f"已生成山东词典: {dict_path}")

    # 增强停用词表，剔除数字、序号、评分、无关词、英文、符号
    stopwords = set([
        '附录', '规范性', '管理局', '大项', '小项', '分项',
        '自检', '合计', '根据', '为了', '应当', '按照',
        '关于', '所示', '（', '）', '【', '】', '·', '、', '；', '：',
        '打印', '关闭', '各级政府网', '直属单位网站',
        '评分', '得分', '分数', '级别', '项目', '单位', '序号', '标准', 'DB37', '主要', '以上', '以下', '分', '项', '小项', '大项',
        '1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '4.3',
        '之一', '低于', '影响', '造成', '突出', '工作', '情况', '问题', '相关', '社会', '服务', '管理', '单位', '部门', '以上', '以下',
        'html', 'gov', 'cn', 'art', 'GB', '文件', 'whly', 'yantai', 'com', 'www', 'http', 'https',
        '资源', '质量', '适用', '有效', '示范', '加强', '政策', '加分', '市县', '推进', '安全', '有效', '提升', '管理', '服务',
        *[str(i) for i in range(0, 100)],
        *[f"{i}.{j}" for i in range(0, 10) for j in range(0, 10)]
    ])

    # 分词处理（启用HMM识别长术语）
    words = list(jieba.cut(text, cut_all=False, HMM=True))
    print(f"山东政策分词后总词汇数: {len(words)}")

    # 过滤停用词并保留核心词和白名单
    filtered_words = []
    for word in words:
        if word in custom_words or word in whitelist:
            filtered_words.append(word)
            continue
        if word in stopwords or len(word) == 1:
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

    with open('shandong_segmented_words.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(filtered_words))
    print("山东政策分词结果已保存")

    return filtered_words, custom_words, whitelist


# ====================== 2. 伪多文档生成：适配山东政策结构 ======================
def generate_pseudo_documents(words, custom_words, num_docs=12, chunk_size=60):
    """用全部分词结果生成伪文档，保证主题分析词量充足"""
    if len(words) < chunk_size:
        raise ValueError(f"山东分词结果过短({len(words)})，无法生成伪文档")

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

    print(f"生成{num_docs}篇山东伪文档，每篇约{chunk_size}词")
    return pseudo_docs


# ====================== 3. LDA模型：适配山东7大政策模块 ======================
def build_shandong_lda_model(documents, num_topics=7):
    """针对山东政策7大模块优化LDA参数"""
    dictionary = corpora.Dictionary(documents)
    # 过滤低频词，保留山东特有术语
    dictionary.filter_extremes(no_below=3, no_above=0.9)
    print(f"山东词典尺寸: {len(dictionary)}，包含核心评定术语")

    corpus = [dictionary.doc2bow(doc) for doc in documents]
    if not corpus or sum(len(c) for c in corpus) == 0:
        raise ValueError("山东语料库为空，请检查分词结果")

    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        alpha=0.1,  # 增强主题区分度
        eta=0.02,  # 提高词分布稀疏性
        passes=150,  # 确保政策术语收敛
        random_state=42
    )

    # 打印山东主题关键词（检查模块划分）
    print("\n===== 山东全域旅游政策主题关键词 =====")
    for i in range(num_topics):
        topic_words = lda.show_topic(i, topn=6)
        print(f"主题{i} ({'|'.join([w for w, _ in topic_words[:3]])}): {topic_words}")

    return lda, dictionary, corpus


def optimize_lda_topics(documents, max_topics=12):
    """通过困惑度曲线确定最佳主题数，匹配山东政策模块"""
    print("\n===== 计算不同主题数的困惑度 =====")
    perplexities = []
    topics_range = range(2, max_topics + 1)  # 主题数范围设为2到12

    # 预处理文档
    dictionary = corpora.Dictionary(documents)
    dictionary.filter_extremes(no_below=3, no_above=0.9)
    corpus = [dictionary.doc2bow(doc) for doc in documents]

    for k in topics_range:
        try:
            print(f"正在训练主题数为{k}的LDA模型...")
            lda = models.LdaModel(
                corpus=corpus,
                id2word=dictionary,
                num_topics=k,
                alpha=0.1,
                eta=0.02,
                passes=50,  # 为加速计算，降低迭代次数
                random_state=42
            )
            perplexity = lda.log_perplexity(corpus)  # 计算困惑度，越小越好
            perplexities.append((k, perplexity))
            print(f"主题数{k}的困惑度: {perplexity:.2f}")
        except Exception as e:
            print(f"训练主题数{k}的LDA模型时出错: {str(e)}")
            perplexities.append((k, float('inf')))  # 出错时设为无穷大

    # 绘制困惑度曲线
    plot_perplexity_curve(perplexities)

    # 选择困惑度最低的主题数
    optimal_k, _ = min(perplexities, key=lambda x: x[1])
    print(f"\n推荐的最佳主题数: {optimal_k}")

    # 考虑山东政策的7大模块，若计算出的主题数与7相差较大，给出提示
    if abs(optimal_k - 7) > 2:
        print(f"注意: 计算出的最佳主题数{optimal_k}与山东政策的7大模块差异较大，可能需要调整")

    return optimal_k


# ====================== 4. 新增：困惑度曲线绘制功能 ======================
def plot_perplexity_curve(perplexities):
    """绘制困惑度随主题数变化的曲线"""
    topics, perplexity_values = zip(*perplexities)
    perplexity_values = [-p for p in perplexity_values]  # 转换为正值以便绘制

    plt.figure(figsize=(10, 6), dpi=150)
    plt.plot(topics, perplexity_values, 'o-', linewidth=2, color='navy')
    plt.scatter(topics, perplexity_values, s=100, color='red', zorder=5)


    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlabel('主题数', fontsize=12)
    plt.ylabel('困惑度（取反，值越小模型越好）', fontsize=12)
    plt.title('山东全域旅游政策LDA模型困惑度曲线', fontsize=14)
    plt.xticks(topics)
    plt.tight_layout()
    plt.savefig('shandong_perplexity_curve.png', dpi=150, bbox_inches='tight')
    print("困惑度曲线图已保存为 shandong_perplexity_curve.png")


# ====================== 4. 可视化：优化山东政策主题展示 ======================
def plot_shandong_topic_radar(lda, dictionary, topic_names):
    """绘制山东政策主题雷达图，控制尺寸在合理范围"""
    topic_weights = []
    for topic_id in range(lda.num_topics):
        alpha = lda.alpha[topic_id] if hasattr(lda, 'alpha') else 1 / lda.num_topics
        topic_words = lda.show_topic(topic_id, topn=5)
        word_probs = sum(p for _, p in topic_words)
        topic_weights.append(alpha * word_probs)

    # 归一化权重并控制范围
    topic_weights = np.array(topic_weights) / np.max(topic_weights) * 700

    # 按山东政策模块顺序排列
    shandong_order = [
        "城乡旅游环境", "旅游公共服务", "旅游发展效益",
        "综合竞争力", "产业融合发展", "保障机制建设", "评分标准体系"
    ]
    # 保证topic_names长度与lda.num_topics一致
    if len(shandong_order) < lda.num_topics:
        topic_names = shandong_order + [f"扩展主题{i+1}" for i in range(lda.num_topics - len(shandong_order))]
    else:
        topic_names = shandong_order[:lda.num_topics]

    angles = np.linspace(0, 2 * np.pi, len(topic_names), endpoint=False).tolist()
    topic_weights = np.concatenate((topic_weights, [topic_weights[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), dpi=150, subplot_kw=dict(polar=True))
    ax.plot(angles, topic_weights, 'o-', linewidth=2, color='navy', label='主题权重')
    ax.fill(angles, topic_weights, alpha=0.15, color='navy')
    ax.set_thetagrids(np.degrees(angles[:-1]), topic_names, fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize=8)
    plt.title('山东全域旅游示范市县评定标准主题分布雷达图', fontsize=14, pad=20)
    plt.savefig('shandong_topic_radar.png', dpi=150, bbox_inches='tight')


def build_topic_cooccurrence_network(lda, dictionary, topn=12):
    """构建山东政策主题-关键词共现网络，只保留白名单和自定义词典中的高频词"""
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

    # 添加节点
    for word, topic_id in all_topic_words:
        G.add_node(word, type='keyword', topic=topic_id)
    for topic_id in range(lda.num_topics):
        G.add_node(f"山东主题{topic_id}", type='topic', topic=topic_id)

    # 添加边（主题-关键词，关键词-关键词）
    for topic_id in range(lda.num_topics):
        topic_name = f"山东主题{topic_id}"
        topic_words = [word for word, _ in lda.show_topic(topic_id, topn=topn) if len(word) > 1 and (word in custom_words or word in whitelist) and re.fullmatch(r'[\u4e00-\u9fff]+', word)]
        topic_words = [w for w in topic_words if word_counts[w] > 1]
        for word in topic_words:
            G.add_edge(topic_name, word, weight=1)
        for i in range(len(topic_words)):
            for j in range(i + 1, len(topic_words)):
                w1, w2 = topic_words[i], topic_words[j]
                if G.has_edge(w1, w2):
                    G[w1][w2]['weight'] += 1
                else:
                    G.add_edge(w1, w2, weight=1)

    # 可视化参数
    plt.figure(figsize=(12, 10), dpi=150)
    pos = nx.circular_layout(G, scale=1)
    node_sizes = []
    node_colors = []

    for node in G.nodes():
        if node.startswith("山东主题"):
            node_sizes.append(5000)
            node_colors.append(f"C{int(node[-1])}")
        else:
            node_sizes.append(max(400, len([w for w, _ in all_topic_words if w == node]) * 200))
            node_colors.append(f"C{G.nodes[node]['topic']}")

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.8)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w * 0.4 for w in edge_weights], alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(
        G, pos,
        font_size=8, font_family='Microsoft YaHei',
        font_weight='bold' if node.startswith("山东主题") else 'normal'
    )

    plt.title('山东全域旅游政策主题-关键词共现网络', fontsize=12)
    plt.axis('off')
    plt.savefig('shandong_cooccurrence_network.png', dpi=150, bbox_inches='tight')
    return G


def visualize_lda_topics(lda, dictionary, corpus):
    """生成LDAvis可视化，彻底修复complex128序列化报错"""
    import numpy as np
    import pyLDAvis
    import pyLDAvis.gensim_models
    import json

    # patch json encoder，自动将complex128、float、int转为float/int
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.complexfloating):
                return float(np.real(obj))
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.integer):
                return int(obj)
            return super(NumpyEncoder, self).default(obj)
    json._default_encoder = NumpyEncoder()

    vis_data = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(vis_data, 'shandong_lda_visualization.html')
    print("山东LDAvis交互式可视化已保存")


# ====================== 5. 量化指标计算 ======================
def calculate_topic_entropy(lda):
    topic_dist = lda.alpha / lda.alpha.sum()
    return entropy(topic_dist)


def calculate_topic_concentration(lda):
    topic_dist = lda.alpha / lda.alpha.sum()
    sorted_dist = np.sort(topic_dist)[::-1]
    return sorted_dist[:3].sum()


# ====================== 5. 主函数：全链路山东政策分析 ======================
def analyze_shandong_policy(file_path):
    """分析山东全域旅游政策文档，返回LDA模型"""
    try:
        print("\n\n==================== 山东全域旅游政策分析启动 ====================")

        # 1. 读取山东PDF文档
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"山东文档不存在: {file_path}")
        text = extract_shandong_text(file_path)
        if len(text) < 3000:
            raise ValueError("山东文档内容读取异常，请检查PDF格式")

        # 2. 文本预处理
        words, custom_words, whitelist = preprocess_text(text)

        # 3. 生成伪文档
        pseudo_docs = generate_pseudo_documents(words, custom_words, num_docs=12, chunk_size=60)

        # 4. 主题建模
        print("\n===== 山东LDA模型训练 =====")
        optimal_k = optimize_lda_topics(pseudo_docs)
        lda, dictionary, corpus = build_shandong_lda_model(pseudo_docs, optimal_k)

        # 5. 定义主题名称
        shandong_topics = [
            "城乡旅游环境", "旅游公共服务", "旅游发展效益",
            "综合竞争力", "产业融合发展", "保障机制建设", "评分标准体系"
        ]
        topic_names = shandong_topics[:lda.num_topics]
        print(f"使用山东政策主题: {topic_names}")

        # 6. 可视化（优化尺寸和元素）
        print("\n===== 生成山东政策可视化图表 =====")
        plot_shandong_topic_radar(lda, dictionary, topic_names)
        build_topic_cooccurrence_network(lda, dictionary)
        visualize_lda_topics(lda, dictionary, corpus)
        print("可视化图表已生成，尺寸已优化")

        # 7. 量化指标
        entropy_val = calculate_topic_entropy(lda)
        concentration_val = calculate_topic_concentration(lda)
        print(f"\n===== 山东政策量化分析结果 =====")
        print(f"主题熵值: {entropy_val:.2f}")
        print(f"主题集中度: {concentration_val:.2f}")

        print("\n==================== 山东政策分析完成！ ====================")
        print("重点输出:")
        print("- shandong_segmented_words.txt → 核心词验证")
        print("- shandong_perplexity_curve.png → 困惑度曲线（新增）")
        print("- shandong_topic_radar.png → 主题权重分布")
        print("- shandong_cooccurrence_network.png → 术语关联关系")
        print("- shandong_lda_visualization.html → 交互式主题探索")
        return lda

    except Exception as e:
        print(f"\n==================== 山东政策分析失败！ ====================")
        print(f"错误详情: {str(e)}")
        return None


# ====================== 执行入口：指定山东文档路径 ======================
if __name__ == "__main__":
    # 替换为实际山东PDF路径
    file_path = SOURCE_DOC_DIR / "山东 全域旅游示范市县评定标准（2017修订）.pdf"
    lda_model = analyze_shandong_policy(file_path)
    if lda_model is None:
        print("❗山东政策分析终止→ 请检查错误并重新运行")