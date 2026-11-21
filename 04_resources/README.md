# 04_resources · 资源

## data/DATA.md

**数据获取与模拟指南**，回答「数据从哪来」这个问题：

- 哪些数据随仓库提供、哪些需要自行获取、哪些用合成数据替代
- 每个数据集的具体来源、许可与获取路径
- `tools/simulate_data.py` 的用法与生成字段

## datasets

原 `data/datasets/Multi30k/` 只有两个未下载完成的占位文件
（`training.tar.gz.promise.*`），实际数据从未落地，已移入本地归档目录，未随仓库公开。

需要 Multi30k 时按官方方式重新下载：

```
https://www.statmt.org/wmt16/multimodal-task.html
```

其余小型数据集直接放在各自项目目录内，见：

- `01_coursework/machine-learning/dating.txt`、`factor_returns.csv`
- `01_coursework/text-mining/《人工智能导论》评论（作业）.xls`
- `03_research/misc-figures/preprocessed_rfm_data.xlsx`
