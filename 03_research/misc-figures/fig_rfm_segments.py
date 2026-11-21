import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义数据
data = [
    (1, 1, 1, "重要价值用户", "20.0%"),
    (1, 0, 1, "重要保持用户", "8.0%"),
    (0, 1, 1, "重要发展用户", "9.3%"),
    (0, 0, 1, "重要挽留用户", "16.0%"),
    (1, 1, 0, "一般价值用户", "9.3%"),
    (1, 0, 0, "一般保持用户", "13.3%"),
    (0, 1, 0, "一般发展用户", "4.0%"),
    (0, 0, 0, "一般挽留用户", "20.0%")
]

# 创建 3D 图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制坐标轴标签
ax.set_xlabel('R 价值类别', fontsize=15, labelpad=5)
ax.set_ylabel('F 价值类别', fontsize=15, labelpad=5)
ax.set_zlabel('M 价值类别', fontsize=15, labelpad=5)

# 定义 R、F、M 的取值范围，以0.1为间隔
r_values = np.arange(0, 1.1, 0.1)
f_values = np.arange(0, 1.1, 0.1)
m_values = np.arange(0, 1.1, 0.1)

# 绘制网格线
for r in r_values:
    for f in f_values:
        for m in m_values:
            ax.plot([r, r], [f, f], [m, m], 'k-', alpha=0.1)

# 定义颜色列表（浅红色、浅橙色、浅黄色）
colors = ['#FFB6C1', '#FFA07A', '#FFFFCC']
color_index = 0

# 绘制透明平面，颜色改为更深的珊瑚色 '#F08080'
xx, yy = np.meshgrid([0, 1], [0, 1])
ax.plot_surface(xx, yy, np.full_like(xx, 0), alpha=0.2, color='#F08080')
ax.plot_surface(xx, yy, np.full_like(xx, 1), alpha=0.2, color='#F08080')
ax.plot_surface(xx, np.full_like(xx, 0), yy, alpha=0.2, color='#F08080')
ax.plot_surface(xx, np.full_like(xx, 1), yy, alpha=0.2, color='#F08080')
ax.plot_surface(np.full_like(xx, 0), xx, yy, alpha=0.2, color='#F08080')
ax.plot_surface(np.full_like(xx, 1), xx, yy, alpha=0.2, color='#F08080')

# 绘制数据点并标注，放大数据标签字体
for r, f, m, user_type, ratio in data:  # 这里改为 5 个变量
    color = colors[color_index % len(colors)]
    ax.scatter(r, f, m, marker='o', s=200, color=color, edgecolor='k', alpha=0.8)
    ax.text(r + 0.1, f + 0.1, m + 0.1, f"{user_type}\n占比: {ratio}",  # 这里去除对 num 的引用
            ha='left', va='bottom', fontsize=15)
    color_index += 1

# 调整刻度和视角
ax.set_xlim(-0.2, 1.2)
ax.set_ylim(-0.2, 1.2)
ax.set_zlim(-0.2, 1.2)
ax.set_xticks(np.arange(0, 1.1, 0.1))
ax.set_yticks(np.arange(0, 1.1, 0.1))
ax.set_zticks(np.arange(0, 1.1, 0.1))
ax.view_init(elev=20, azim=30)

# 加粗放大坐标轴并设置颜色，添加箭头
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis._axinfo["tick"]["inward_factor"] = 0
ax.xaxis._axinfo["tick"]["outward_factor"] = 0.5
ax.yaxis._axinfo["tick"]["inward_factor"] = 0
ax.yaxis._axinfo["tick"]["outward_factor"] = 0.5
ax.zaxis._axinfo["tick"]["inward_factor"] = 0
ax.zaxis._axinfo["tick"]["outward_factor"] = 0.5
ax.xaxis.line.set_color("#0072BD")  # 更美观的颜色
ax.yaxis.line.set_color("#D95319")
ax.zaxis.line.set_color("#449D44")
ax.xaxis.line.set_linewidth(2)  # 加粗
ax.yaxis.line.set_linewidth(2)
ax.zaxis.line.set_linewidth(2)
ax.tick_params(axis='x', colors="#0072BD", labelsize=12)  # 放大刻度字体
ax.tick_params(axis='y', colors="#D95319", labelsize=12)
ax.tick_params(axis='z', colors="#449D44", labelsize=12)

# 去除网格线背景
ax.grid(False)

# 显示图形
plt.tight_layout()
plt.show()