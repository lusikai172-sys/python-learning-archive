# 02_practice · 练习代码

非作业性质的试验代码，用于验证某个库或某个想法能不能跑通。

## deep-learning

`day01_deep learning.py`：TensorFlow 1.x 的图（Graph）与会话（Session）机制演示。
用 `tf.compat.v1.disable_v2_behavior()` 关闭 TF2 的即时执行，模拟 1.x 写法。

```bash
pip install tensorflow
python "02_practice/deep-learning/day01_deep learning.py"
```

## jupyter-notebooks

| Notebook | 内容 |
|---|---|
| `day01_instacart_pca.ipynb` | Instacart 数据的 PCA 降维 |
| `day02_titanic_demo.ipynb` | Titanic 数据初步处理 |
| `day03_cancer_demo.ipynb` | 乳腺癌数据集建模（含完整输出与报错记录） |

直接用 Jupyter 打开即可，`day03` 依赖 scikit-learn 自带的 `load_breast_cancer`。

## visualization

| 脚本 | 内容 | 数据 |
|---|---|---|
| `new.py` | 网约车按小时出行量柱状图（pyecharts） | `data/train_new2.csv` |
| `zhengli.py` | 地震数据 XGBoost 回归 + 纬度趋势拟合 | `data/中国地震数据（2012-2024）_ppman.xlsx` |

`zhengli.py` 原先 `from scipy import polyfit, poly1d`，该接口在 SciPy 1.3 后已移除，
现改为 `from numpy import poly1d`（`np.polyfit` 本来就是 numpy 的）。

数据放进 `data/`，或用 `VIS_DATA_DIR` 指定目录。
