import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 移除中文字体设置，使用默认英文字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 调整seaborn字体设置
sns.set(font_scale=1.0)

# 确保图表风格美观
sns.set_style("whitegrid")
sns.set_palette("viridis")

# 1. 页面加载时间优化效果
plt.figure(figsize=(8, 7))

# 生成模拟数据 - 优化前后的页面加载时间对比
optimization_stages = ['Before Optimization', 'Image Compression', 'Code Minimization', 'CDN Acceleration', 'Final Optimization']
load_times = [3.8, 2.9, 2.1, 1.5, 1.2]

plt.plot(optimization_stages, load_times, 'o-', linewidth=2.5, markersize=8)
plt.title('Page Load Time Optimization', fontsize=14)
plt.ylabel('Load Time (seconds)', fontsize=12)
plt.ylim(0, 4)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=15)

# 添加数值标签
for i, txt in enumerate(load_times):
    plt.annotate(f'{txt}s', (i, load_times[i]), xytext=(0, 5),
                 textcoords='offset points', ha='center', fontsize=10)

plt.tight_layout()
plt.show()  # 显示第一个图表，等待关闭

# 2. 用户操作路径简化效果
plt.figure(figsize=(8, 7))

# 生成模拟数据 - 完成核心任务所需步骤
tasks = ['Account Registration', 'Product Purchase', 'Information Inquiry', 'Issue Feedback']
before_optimization = [7, 5, 4, 6]
after_optimization = [3, 2, 2, 3]

x = np.arange(len(tasks))
width = 0.35

plt.bar(x - width/2, before_optimization, width, label='Before Optimization')
plt.bar(x + width/2, after_optimization, width, label='After Optimization')

plt.title('Steps to Complete Core Tasks', fontsize=14)
plt.ylabel('Number of Steps', fontsize=12)
plt.xticks(x, tasks, rotation=15)
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()  # 显示第二个图表，等待关闭

# 3. 用户满意度提升
plt.figure(figsize=(8, 7))

# 生成模拟数据 - 用户满意度评分
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
satisfaction_scores = [72, 73, 85, 88, 92, 94]

plt.bar(months, satisfaction_scores, color='skyblue')
plt.title('User Satisfaction Trend', fontsize=14)
plt.ylabel('Satisfaction Score (0-100)', fontsize=12)
plt.ylim(60, 100)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 添加数值标签
for i, v in enumerate(satisfaction_scores):
    plt.text(i, v + 1, str(v), ha='center', fontsize=10)

plt.tight_layout()
plt.show()  # 显示第三个图表，等待关闭

# 4. 转化率提升效果 - 雷达图
plt.figure(figsize=(8, 7))
ax = plt.subplot(111, polar=True)  # 创建极坐标子图

# 生成模拟数据 - 优化前后的转化率对比
conversion_types = ['View-Click', 'Click-Add to Cart', 'Add to Cart-Purchase', 'Purchase-Repeat Purchase']
before_conv = [25, 15, 8, 3]
after_conv = [38, 28, 18, 10]

# 绘制雷达图
labels = conversion_types
stats_before = before_conv
stats_after = after_conv

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()

# 闭合雷达图
stats_before = np.concatenate((stats_before, [stats_before[0]]))
stats_after = np.concatenate((stats_after, [stats_after[0]]))
angles = angles + [angles[0]]
labels = labels + [labels[0]]

ax.plot(angles, stats_before, 'o-', linewidth=2, label='Before Optimization')
ax.fill(angles, stats_before, alpha=0.25)
ax.plot(angles, stats_after, 'o-', linewidth=2, label='After Optimization')
ax.fill(angles, stats_after, alpha=0.25)

ax.set_thetagrids(np.degrees(angles), labels, rotation=0)
ax.set_ylim(0, 40)
ax.set_title('Conversion Funnel Optimization', fontsize=14)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.show()  # 显示第四个图表，等待关闭
