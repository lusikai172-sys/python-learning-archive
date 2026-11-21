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


# ====================== 1. 文本预处理：强化PDF表格与章节提取 ======================
def extract_pdf_text(file_path):
    """提取PDF文本并强化表格、章节编号保留（参考江西DOCX处理逻辑）"""
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            full_text = []
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ''

                # 1. 提取表格内容（模拟江西表格处理）
                table_text = re.findall(r'\|\s*([^\|]*)\s*\|\n', page_text)
                full_text.extend(table_text)

                # 2. 提取普通文本并处理章节编号
                normal_text = re.sub(r'\|\s*[^\|]*\s*\|\n', '', page_text)
                normal_text = re.sub(r'(\d+\.\d+\.\d+)', r'\n\1 ', normal_text)  # 三级章节
                normal_text = re.sub(r'(\d+\.\d+)', r'\n\1 ', normal_text)  # 二级章节
                full_text.append(normal_text)

            # 3. 合并文本并处理特殊词汇
            combined_text = ' '.join(full_text).replace('全域旅游', '浙江全域旅游')
            return combined_text

    except Exception as e:
        print(f"读取浙江PDF {file_path} 失败: {str(e)}")
        return ""


def preprocess_text(text):
    """优化浙江政策分词逻辑，极大增强停用词过滤，保留全中文高频政策词和白名单词"""
    print(f"浙江政策原始文本总长度: {len(text)}")

    # 浙江全域旅游自定义词典（含核心指标术语）
    dict_path = 'zj_tourism_dict_2023.txt'
    custom_words = [
        '浙江全域旅游', '示范县', '评分细则', '政策支持', '旅游交通',
        '公共服务', '智慧旅游', '旅游环境', '产业融合', '创建申报',
        '大数据中心', '旅游风情小镇', '专项资金', '多规合一', '绿道慢行系统',
        '评定标准', '旅游厕所革命', '红黑榜', '共建共享', '业态融合',
        '游客满意度', '旅游安全', '生态保护', '加分项', '一票否决'
    ]

    # 白名单核心政策词（可根据实际需求补充）
    whitelist = set([
        '交通', '服务', '环境', '融合', '安全', '品牌', '创新', '监管', '满意度', '生态', '旅游', '公共', '智慧', '资源', '市场', '项目', '资金', '政策', '标准', '体系', '机制', '平台', '产品', '发展', '保护', '管理', '宣传', '推广', '引导', '合作', '共享', '监督', '评估', '考核', '激励', '奖惩', '投诉', '应急', '风险', '应对', '规划', '目标', '指标', '责任', '落实', '执行', '实施', '改革', '优化', '提升', '完善', '健全', '规范', '制度', '流程', '程序', '办法', '措施', '方案', '计划', '总结', '报告', '通报', '反馈', '建议', '意见', '决策', '指令', '命令', '通知', '公告', '公示', '声明', '说明', '解读', '解答', '咨询', '支持', '帮助', '指导', '培训', '教育'
    ])

    # 加载或生成词典
    if os.path.exists(dict_path):
        jieba.load_userdict(dict_path)
        print(f"已加载浙江自定义词典: {dict_path}")
        with open(dict_path, 'r', encoding='utf-8') as f:
            custom_words.extend([line.strip() for line in f if line.strip()])
    else:
        with open(dict_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(custom_words))
        jieba.load_userdict(dict_path)
        print(f"已生成浙江2023版词典: {dict_path}")

    # 进一步增强停用词表
    stopwords = set([
        '附录', '大项', '小项', '分项', '自检', '合计',
        '应当', '按照', '关于', '所示', '·', '、', '；', '：', '｜',
        '得分', '扣分', '评价', '之一', '低于', '影响', '造成', '突出', '工作', '情况', '问题', '相关', '社会', '服务', '管理', '单位', '部门', '有效', '示范', '推进', '提升', '加分', '政策', '市县', '安全', '发展', '市州', 'OTA',
        'html', 'gov', 'cn', 'art', 'GB', '文件', 'whly', 'com', 'www', 'http', 'https',
        '以来', '一年', '分数', '典型', '累计', '分别', '重点', '证书', '命名', '文旅', '品牌', '效应', '效益', '社会效益', '经济效益', '国家级', '省级', '市州', '县区', '乡村', '年度', '年内', '年末', '年初', '年均', '年增长', '年减少', '年平均', '年累计', '年分', '年报', '年终', '年初', '年终', '年终奖',
        '企业', '功能', '支持', '主推', '文旅', '体育', '特色', '机制', '团队', '认定', '规划', '环节', '设立', '评估', '加快', '推进', '项目', '设立', '规划', '评估', '加快', '推进', '企业', '功能', '支持', '主推', '文旅', '体育', '特色', '机制', '团队', '认定', '规划', '环节', '设立', '评估', '加快', '推进',
        *[str(i) for i in range(0, 100)],
        *[f"{i}.{j}" for i in range(0, 10) for j in range(0, 10)]
    ])

    # 分词处理（启用HMM并添加复合词）
    jieba.add_word('浙江全域旅游示范县')
    jieba.add_word('旅游大数据中心')
    jieba.add_word('旅游风情小镇')
    words = list(jieba.cut(text, cut_all=False, HMM=True))
    print(f"浙江政策分词后总词汇数: {len(words)}")

    # 过滤停用词并保留核心词
    filtered_words = []
    for word in words:
        if word in custom_words or word in whitelist:
            filtered_words.append(word)
            continue
        if word in stopwords or len(word) == 1:
            continue
        filtered_words.append(word)
    print(f"初步过滤后词汇数: {len(filtered_words)}")

    # 只保留全中文、长度大于1且在白名单或自定义词典中的词
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

    with open('zj_segmented_words_2023.txt', 'w', encoding='utf-8') as f:
        f.write(' '.join(filtered_words))
    print("浙江2023分词结果已保存至当前目录")

    return filtered_words, custom_words, whitelist


# ====================== 2. 伪文档生成：适配单文档场景 ======================
def generate_pseudo_documents(words, custom_words, num_docs=12, chunk_size=70):
    """按浙江政策模块生成伪文档（参考江西单文档优化）"""
    if len(words) < chunk_size:
        raise ValueError(f"浙江分词结果过短({len(words)})，建议调整chunk_size")

    pseudo_docs = []
    key_segments = []
    current_segment = []
    zj_keywords = [
        "政策支持", "旅游交通", "公共服务", "智慧旅游",
        "旅游环境", "产品体系", "市场监管", "共建共享",
        "安全保障", "加分项", "否决项", "产业经济"
    ]  # 匹配浙江12项核心政策模块

    for word in words:
        current_segment.append(word)
        if word in zj_keywords and len(current_segment) > chunk_size // 2:
            key_segments.append(current_segment)
            current_segment = []

    if current_segment:
        key_segments.append(current_segment)

    # 补全文档数量并添加核心词（参考江西单文档逻辑）
    while len(key_segments) < num_docs:
        sample = np.random.choice(words, size=chunk_size, replace=True).tolist()
        if len(key_segments) % 2 == 0:
            sample.extend(np.random.choice(custom_words, size=2, replace=False).tolist())
        key_segments.append(sample)

    # 确保每个文档包含政策核心模块
    for i in range(num_docs):
        np.random.shuffle(key_segments[i])
        if i % 3 == 0 and custom_words:
            core_modules = np.random.choice(zj_keywords, size=2, replace=False).tolist()
            key_segments[i].extend(core_modules)
        pseudo_docs.append(key_segments[i])

    print(f"生成{num_docs}篇浙江伪文档，每篇约{chunk_size}词，包含政策模块")
    return pseudo_docs


# ====================== 3. LDA模型：适配浙江12项政策模块 ======================
def build_zj_lda_model(documents, num_topics=12):
    """针对浙江政策模块调整主题模型（参考江西12指标逻辑）"""
    dictionary = corpora.Dictionary(documents)
    dictionary.filter_extremes(no_below=3, no_above=0.9)
    print(f"浙江词典尺寸: {len(dictionary)}，包含政策核心术语")

    corpus = [dictionary.doc2bow(doc) for doc in documents]
    if not corpus:
        raise ValueError("浙江语料库为空，请检查分词结果")

    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        alpha=0.18,  # 单文档场景提高主题区分度
        eta=0.025,  # 增强稀疏性
        passes=150,  # 减少迭代
        random_state=42
    )

    # 打印浙江政策主题关键词
    print("\n===== 浙江2023政策主题关键词 =====")
    for i in range(min(5, num_topics)):
        topic_words = lda.show_topic(i, topn=8)
        print(f"主题{i} ({'|'.join([w for w, _ in topic_words[:3]])}): {topic_words}")

    return lda, dictionary, corpus


def optimize_lda_topics(documents, max_topics=12):
    """优化主题数适配浙江12项政策模块"""
    perplexity_scores = []
    for k in range(6, max_topics + 1):  # 从6开始搜索
        try:
            lda, _, corpus = build_zj_lda_model(documents, k)
            perplexity = lda.log_perplexity(corpus)
            perplexity_scores.append((k, perplexity))
            print(f"浙江主题数{k} → 困惑度{perplexity:.4f}")
        except Exception as e:
            print(f"浙江主题数{k}训练失败: {str(e)}")

    if not perplexity_scores:
        print("警告：浙江所有主题数训练失败，强制使用主题数10")
        return 10

    # 绘制困惑度曲线（参考江西样式）
    plt.figure(figsize=(10, 6))
    k_list = [p[0] for p in perplexity_scores]
    perp_list = [p[1] for p in perplexity_scores]
    plt.plot(k_list, perp_list, 'o-', color='darkgreen')
    plt.xticks(k_list)
    plt.xlabel('主题数量', fontsize=12)
    plt.ylabel('困惑度', fontsize=12)
    plt.title('浙江2023旅游政策LDA主题数优化', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig('zj_topic_perplexity_2023.png', dpi=300)

    # 选择拐点并确保主题数合理
    if len(perplexity_scores) >= 3:
        diffs = np.diff(perp_list)
        min_diff_idx = np.argmin(diffs)
        optimal_k = k_list[min_diff_idx + 1]
        optimal_k = max(8, optimal_k)  # 最低主题数
    else:
        optimal_k = 10
    print(f"自动选择浙江2023最优主题数: {optimal_k}")
    return optimal_k


# ====================== 4. 可视化：适配江西可视化效果 ======================
def plot_zj_topic_radar(lda, dictionary, topic_names):
    """绘制浙江政策主题雷达图（参考江西样式）"""
    topic_weights = []
    for topic_id in range(lda.num_topics):
        alpha = lda.alpha[topic_id] if hasattr(lda, 'alpha') else 1 / lda.num_topics
        topic_words = lda.show_topic(topic_id, topn=10)
        word_probs = sum(p for _, p in topic_words)
        topic_weights.append(alpha * word_probs)

    # 归一化权重
    topic_weights = np.array(topic_weights) / np.max(topic_weights) * 900

    # 雷达图绘制（浙江政策模块顺序）
    zj_order = [
        "1. 政策支持", "2. 旅游交通", "3. 公共服务", "4. 智慧旅游",
        "5. 旅游环境", "6. 产品体系", "7. 市场监管", "8. 共建共享",
        "9. 安全保障", "10. 产业经济", "11. 加分项", "12. 否决项"
    ]
    topic_names = zj_order[:lda.num_topics]
    angles = np.linspace(0, 2 * np.pi, len(topic_names), endpoint=False).tolist()
    topic_weights = np.concatenate((topic_weights, [topic_weights[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(16, 16), subplot_kw=dict(polar=True))
    ax.plot(angles, topic_weights, 'o-', linewidth=3, color='darkblue', label='主题权重')
    ax.fill(angles, topic_weights, alpha=0.2, color='darkblue')
    ax.set_thetagrids(np.degrees(angles[:-1]), topic_names, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize=12)
    plt.title('浙江全域旅游示范县(2023)政策主题分布雷达图', fontsize=18, pad=30)
    plt.savefig('zj_topic_radar_2023.png', dpi=300)


def build_topic_cooccurrence_network(lda, dictionary, topn=18):
    """构建浙江政策主题-关键词共现网络，只保留白名单和自定义词典中的高频词"""
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
        G.add_node(f"浙江主题{topic_id}", type='topic', topic=topic_id)

    # 添加边
    for topic_id in range(lda.num_topics):
        topic_name = f"浙江主题{topic_id}"
        topic_words = [word for word, _ in lda.show_topic(topic_id, topn=topn) if len(word) > 1 and (word in custom_words or word in whitelist) and re.fullmatch(r'[\u4e00-\u9fff]+', word)]
        # 只保留高频词
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

    # 可视化设置
    plt.figure(figsize=(18, 14))
    pos = nx.circular_layout(G, scale=2)
    node_sizes = []
    node_colors = []

    for node in G.nodes():
        if node.startswith("浙江主题"):
            node_sizes.append(8000)
            node_colors.append(f"C{int(node[-1])}")
        else:
            node_sizes.append(max(500, len([w for w, _ in all_topic_words if w == node]) * 400))
            node_colors.append(f"C{G.nodes[node]['topic']}")

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[w * 0.6 for w in edge_weights], alpha=0.6, edge_color='gray')
    nx.draw_networkx_labels(
        G, pos,
        font_size=10, font_weight='bold',
        font_family='Microsoft YaHei'
    )

    plt.title('浙江2023旅游政策主题-关键词共现网络', fontsize=18)
    plt.axis('off')
    plt.savefig('zj_cooccurrence_network_2023.png', dpi=300)
    return G


def visualize_lda_topics(lda, dictionary, corpus):
    """生成LDAvis可视化，处理复数参数问题"""
    try:
        # 检查并处理LDA模型中的复数参数
        for i in range(len(lda.state.get_lambda())):
            for j in range(len(lda.state.get_lambda()[i])):
                if np.iscomplex(lda.state.get_lambda()[i][j]):
                    lda.state.get_lambda()[i][j] = np.real(lda.state.get_lambda()[i][j])

        # 确保corpus不包含复数
        for doc in corpus:
            for i in range(len(doc)):
                if isinstance(doc[i][1], complex):
                    doc[i] = (doc[i][0], np.real(doc[i][1]))

        # 生成可视化
        vis_data = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, sort_topics=False)
        pyLDAvis.save_html(vis_data, 'zj_lda_visualization_2023.html')
        print("浙江2023 LDAvis交互式可视化已保存")
    except Exception as e:
        print(f"生成LDA可视化失败: {str(e)}")
        print("尝试使用备选方法...")
        try:
            # 备选方法：使用numpy的real函数处理所有复数
            def handle_complex(x):
                if isinstance(x, complex):
                    return np.real(x)
                return x

            # 复制并处理lda参数
            lda_copy = lda
            lda_copy.state.sstats = np.real(lda_copy.state.sstats)

            vis_data = pyLDAvis.gensim_models.prepare(lda_copy, corpus, dictionary, sort_topics=False)
            pyLDAvis.save_html(vis_data, 'zj_lda_visualization_2023_alt.html')
            print("已使用备选方法生成LDA可视化")
        except Exception as e2:
            print(f"备选方法也失败: {str(e2)}")
            print("请检查模型参数或尝试更新pyLDAvis库")


# ====================== 5. 主函数：全链路浙江政策分析 ======================
def analyze_zj_policy(file_path):
    """分析浙江全域旅游政策文档（单文档优化）"""
    try:
        print("\n\n==================== 浙江全域旅游示范县(2023)政策分析启动 ====================")

        # 1. 读取浙江单个PDF文档
        all_text = extract_pdf_text(file_path)
        if not all_text:
            raise ValueError("浙江PDF内容读取失败")

        # 2. 文本预处理
        words, custom_words, whitelist = preprocess_text(all_text)

        # 3. 生成伪文档（单文档场景优化）
        pseudo_docs = generate_pseudo_documents(words, custom_words, num_docs=12, chunk_size=70)

        # 4. 主题建模
        print("\n===== 浙江2023 LDA模型训练 =====")
        optimal_k = optimize_lda_topics(pseudo_docs)
        lda, dictionary, corpus = build_zj_lda_model(pseudo_docs, optimal_k)

        # 5. 定义主题名称（匹配浙江政策模块）
        zj_topics = [
            "1. 政策支持体系", "2. 旅游交通网络", "3. 公共服务建设", "4. 智慧旅游发展",
            "5. 旅游环境优化", "6. 产品体系构建", "7. 市场监管机制", "8. 共建共享机制",
            "9. 安全保障体系", "10. 产业经济指标", "11. 加分项分析", "12. 否决项监控"
        ]
        topic_names = zj_topics[:lda.num_topics]
        print(f"使用浙江2023政策主题: {topic_names}")

        # 6. 可视化（参考江西样式）
        plot_zj_topic_radar(lda, dictionary, topic_names)
        build_topic_cooccurrence_network(lda, dictionary)
        visualize_lda_topics(lda, dictionary, corpus)

        # 7. 量化指标
        entropy_val = calculate_topic_entropy(lda)
        concentration_val = calculate_topic_concentration(lda)
        print(f"\n===== 浙江2023政策量化分析结果 =====")
        print(f"主题熵值: {entropy_val:.2f}（合理范围: 1.8-2.6）")
        print(f"主题集中度: {concentration_val:.2f}（合理范围: 0.7-0.85）")

        print("\n==================== 浙江2023分析完成！建议检查以下内容 ====================")
        print("- zj_segmented_words_2023.txt → 确认2023政策词是否保留")
        print("- 可视化图片 → 检查'智慧旅游'、'共建共享'等主题是否独立")
        print("- zj_lda_visualization_2023.html → 交互式验证政策模块区分度")
        return lda

    except Exception as e:
        print(f"\n==================== 浙江2023分析失败！错误详情 ====================")
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


# ====================== 执行入口：指定浙江文档路径 ======================
if __name__ == "__main__":
    # 单文档路径（浙江2023版）
    file_path = SOURCE_DOC_DIR / "浙江省全域旅游示范县细则.pdf"

    lda_model = analyze_zj_policy(file_path)
    if lda_model is None:
        print("浙江2023分析终止→ 请检查文档路径或调整chunk_size参数")