import re
import os
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import matplotlib.font_manager as font_manager

from pathlib import Path

from config import STOPWORDS_FILE  # noqa: E402

PROJECT_DIR = Path(__file__).resolve().parent

# 设置字体相关（可用 WORDCLOUD_FONT 环境变量指定其他中文字体）
font_path = os.environ.get("WORDCLOUD_FONT", r"C:\Windows\Fonts\simhei.ttf")
# 注册字体，让 matplotlib 能找到并使用该字体
font_manager.fontManager.addfont(font_path)
# 设置 matplotlib 使用该字体，通过更明确的方式获取字体名称来设置
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False


# 数据读取与预处理相关类
class DataProcessor:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.df.dropna(subset=['评论内容'], inplace=True)

    def extract_course_times(self):
        def extract_numbers(s):
            numbers = re.findall(r'\d+', s)
            return ''.join(numbers) if numbers else ''

        self.df['开课次数'] = self.df['第几次课程'].apply(extract_numbers)
        return self.df


class TextPreprocessor:
    def __init__(self, stopwords_path):
        self.stopwords = self.load_stopwords(stopwords_path)
        self.stopwords.update(
            ['的', '了', '在', '是', '我', '你', '他', '她', '它', '我们', '你们', '他们', '这个', '那个', '这些',
             '那些'])

    def load_stopwords(self, stopwords_path):
        try:
            with open(stopwords_path, 'r', encoding='GBK') as f:
                return set(f.read().splitlines())
        except UnicodeDecodeError:
            raise ValueError(f"无法使用utf - 8编码读取停用词文件，文件路径为 {stopwords_path}。")

    def preprocess_text(self):
        def inner(text):
            # 这里先确保文本是字符串类型，防止出现意外类型导致分词等操作出错
            if not isinstance(text, str):
                text = str(text)
            words = jieba.lcut(text)
            filtered_words = [word for word in words if word not in self.stopwords]
            return ' '.join(filtered_words)

        return inner

    def preprocess_dataframe(self, df):
        df['处理后的评论'] = df['评论内容'].apply(self.preprocess_text())
        df = df[df['处理后的评论'].apply(len) > 5]
        return df

    def get_comment_lengths(self, df):
        return df['处理后的评论'].apply(len)


# 自定义基于困惑度的评分函数
def perplexity_score(estimator, X, y=None):
    try:
        lda = estimator
        lda_perplexity = lda.perplexity(X)
        return lda_perplexity
    except:
        return np.inf


# 主题相关操作函数
def find_best_n_components(x, max_n_components=10):
    param_grid = {'n_components': range(2, max_n_components + 1)}
    lda_search = GridSearchCV(LatentDirichletAllocation(random_state=0), param_grid, cv=5, scoring=perplexity_score)
    lda_search.fit(x)
    return lda_search.best_params_['n_components']


def extract_topics(x, n_components):
    lda = LatentDirichletAllocation(n_components=n_components, random_state=0)
    lda.fit(x)
    return lda


def get_topic_words(lda, feature_names, n_top_words=10):
    topic_words = []
    for idx, topic in enumerate(lda.components_):
        top_words = [(feature_names[i], topic[i]) for i in topic.argsort()[-n_top_words - 1:-1]]
        topic_words.append(top_words)
    return topic_words


def get_topic_distributions_by_course_times(df, lda, x, n_components):
    course_times = df['开课次数'].unique()
    distributions = {}
    for time in course_times:
        group_x = x[df['开课次数'] == time]
        if not group_x.shape[0]:
            continue
        group_lda = LatentDirichletAllocation(n_components=n_components, random_state=0).fit(group_x)
        distributions[time] = group_lda.transform(group_x).mean(axis=0)
    return distributions


# 可视化主题词频率直方图的函数
def plot_topic_word_frequency_histograms(topic_words, feature_names):
    num_topics = len(topic_words)
    bar_width = 0.35
    frequency_threshold = 0.2

    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.2)

    for i in range(num_topics):
        topic_dict = {word: weight for word, weight in topic_words[i]}
        high_frequency_topic_words = {word: freq for word, freq in topic_dict.items() if freq > frequency_threshold}
        selected_feature_names = [word for word in feature_names if word in high_frequency_topic_words]
        word_freqs = [high_frequency_topic_words.get(word, 0) for word in selected_feature_names]

        fig, ax = plt.subplots(figsize=(10, 8))
        colors = sns.color_palette("viridis", len(selected_feature_names))
        bars = ax.barh(selected_feature_names, word_freqs, height=bar_width, color=colors, alpha=0.8)

        for bar in bars:
            width = bar.get_width()
            if width > 0:
                ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f"{width:.2f}", ha='left', va='center',
                        fontsize=10, fontproperties=font_prop)

        ax.set_title(f'主题{i + 1} 主题词频率直方图', fontproperties=font_prop)
        ax.set_xlabel('频率', fontproperties=font_prop)
        ax.set_ylabel('主题词', fontproperties=font_prop)

        # 设置y轴刻度标签字体属性
        for label in ax.get_yticklabels():
            label.set_fontproperties(font_prop)

        ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1), fontsize=12, prop=font_prop)
        plt.tight_layout()
        plt.show()


# 绘制分组柱状图展示不同开课次数下各主题的词频情况的函数
def plot_grouped_bar_chart_by_course_times(df, topic_words, feature_names, n_topics):
    course_times = df['开课次数'].unique()
    num_course_times = len(course_times)
    bar_width = 0.2
    x = np.arange(num_course_times)

    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.2)

    fig, ax = plt.subplots(figsize=(12, 8))
    colors = sns.color_palette("Set1", n_topics)

    for topic_idx in range(n_topics):
        topic_dict = {word: weight for word, weight in topic_words[topic_idx]}
        word_freqs_by_time = []
        for time in course_times:
            group_df = df[df['开课次数'] == time]
            group_text = ' '.join(group_df['处理后的评论'].tolist())
            group_word_freqs = [group_text.count(word) for word in feature_names if word in topic_dict]
            word_freqs_by_time.append(sum(group_word_freqs))

        ax.bar(x + topic_idx * bar_width, word_freqs_by_time, width=bar_width, label=f'主题{topic_idx + 1}',
               color=colors[topic_idx], alpha=0.8)

    ax.set_xlabel('开课次数', fontproperties=font_prop)
    ax.set_ylabel('主题词词频', fontproperties=font_prop)
    ax.set_title('不同开课次数下各主题词频情况', fontproperties=font_prop)
    ax.set_xticks(x + (n_topics - 1) * bar_width / 2)
    ax.set_xticklabels(course_times, fontsize=12, fontproperties=font_prop)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fontsize=12, frameon=True, framealpha=0.8,
              prop=font_prop)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # 设置x轴刻度标签字体属性
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)

    # 设置y轴刻度标签字体属性
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_prop)

    plt.tight_layout()
    plt.show()


# 绘制带有数据标签的堆叠条形图展示主题分布情况的函数
def plot_stacked_bar_chart(data, course_times, topic_labels, title):
    index = np.arange(len(course_times))
    bar_width = 0.35
    opacity = 0.8
    colors = sns.color_palette("Set2", len(topic_labels))

    fig, ax = plt.subplots(figsize=(12, 8))
    bottom = np.zeros(len(course_times))
    for i in range(len(topic_labels)):
        ax.bar(index, data[i], bar_width, bottom=bottom, label=topic_labels[i], alpha=opacity, color=colors[i])
        bottom += data[i]

        for j in range(len(course_times)):
            ax.text(j, bottom[j] - data[i][j] / 2, f"{data[i][j]:.2f}", ha='center', va='center', fontsize=10,
                    fontproperties=font_prop)

    ax.set_xlabel('开课次数', fontproperties=font_prop)
    ax.set_ylabel('主题分布（比例）', fontproperties=font_prop)
    ax.set_title(title, fontproperties=font_prop)
    ax.set_xticks(index)
    ax.set_xticklabels(course_times, fontsize=12, fontproperties=font_prop)
    ax.legend(title='主题', loc='upper left', bbox_to_anchor=(1, 1), prop=font_prop)

    # 设置x轴刻度标签字体属性
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)

    # 设置y轴刻度标签字体属性
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_prop)

    plt.tight_layout()
    plt.show()


# 绘制凹凸图展示主题分布随开课次数变化情况的函数
def plot_lineplot_for_topic_distributions(data, course_times, topic_labels, title):
    plot_data = pd.DataFrame(data.T, columns=topic_labels, index=course_times)
    plot_data = plot_data.reset_index().melt(id_vars='index', var_name='主题', value_name='比例')

    plt.figure(figsize=(12, 8))
    sns.pointplot(data=plot_data, x='index', y='比例', hue='主题', palette="Set2", ci="sd", capsize=.2)
    plt.xlabel('开课次数', fontproperties=font_prop)
    plt.ylabel('主题分布（比例）', fontproperties=font_prop)
    plt.title(title, fontproperties=font_prop)

    # 设置x轴刻度标签字体属性
    for label in plt.gca().get_xticklabels():
        label.set_fontproperties(font_prop)

    # 设置y轴刻度标签字体属性
    for label in plt.gca().get_yticklabels():
        label.set_fontproperties(font_prop)

    plt.legend(title='主题', loc='upper left', bbox_to_anchor=(1, 1), prop=font_prop)
    plt.tight_layout()
    plt.show()


# 可视化主题词（词云图）的函数
def visualize_topic_words(topic_words, feature_names):
    for i, topic in enumerate(topic_words):
        topic_dict = {word: weight for word, weight in topic}
        # 明确设置字体路径，确保词云生成时能正确使用字体
        wordcloud = WordCloud(width=800, height=400, background_color='white',
                              font_path=font_path).generate_from_frequencies(topic_dict)

        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'主题{i + 1} 词云图', fontproperties=font_prop)
        plt.axis('off')
        plt.show()


if __name__ == "__main__":
    file_path = PROJECT_DIR / "《人工智能导论》评论（作业）.xls"
    stopwords_path = STOPWORDS_FILE

    # 数据读取与预处理
    data_processor = DataProcessor(file_path)
    df = data_processor.extract_course_times()
    text_preprocessor = TextPreprocessor(stopwords_path)
    df = text_preprocessor.preprocess_dataframe(df)

    # 文本向量化
    vectorizer = TfidfVectorizer(max_features=1000)
    x = vectorizer.fit_transform(df['处理后的评论'])

    # 确定最佳主题数量
    n_topics = find_best_n_components(x)
    print(f"最佳主题数量: {n_topics}")

    # 主题提取
    lda = extract_topics(x, n_topics)
    feature_names = vectorizer.get_feature_names_out()
    topic_words = get_topic_words(lda, feature_names)

    # 可视化主题词（词云图）
    visualize_topic_words(topic_words, feature_names)

    # 绘制主题词频率直方图
    plot_topic_word_frequency_histograms(topic_words, feature_names)

    # 按开课次数分组并提取主题分布
    distributions = get_topic_distributions_by_course_times(df, lda, x, n_topics)
    course_times = sorted(distributions.keys())
    topic_labels = [f'主题{i + 1}' for i in range(n_topics)]
    data = np.array([distributions[time] for time in course_times]).T

    # 绘制分组柱状图展示不同开课次数下各主题词频情况
    plot_grouped_bar_chart_by_course_times(df, topic_words, feature_names, n_topics)

    # 绘制堆叠条形图展示主题分布随开课次数变化情况
    plot_stacked_bar_chart(data, course_times, topic_labels, '《人工智能导论》评论主题随时间变化情况')

    # 绘制凹凸图展示主题分布随开课次数变化情况
    plot_lineplot_for_topic_distributions(data, course_times, topic_labels,
                                          '《人工智能导论》评论主题随时间变化情况（凹凸图）')
