"""省级旅游政策文本 LDA 分析的路径配置。

原始政策文件（docx/pdf）属于外部资料，未随代码归档。
把文件放到任意目录后，通过环境变量 LUO_SOURCE_DIR 指向该目录即可；
默认为原作者的桌面目录，便于在原机器上直接复现。

环境变量：
- LUO_SOURCE_DIR  政策原文所在目录
- LUO_OUTPUT_DIR  图表/分词结果输出目录，默认为脚本所在目录
"""
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
SOURCE_DOC_DIR = Path(
    os.environ.get("LUO_SOURCE_DIR", PROJECT_DIR / "docs")
)
OUTPUT_DIR = Path(os.environ.get("LUO_OUTPUT_DIR", PROJECT_DIR))


def _patch_pyldavis_for_numpy2() -> None:
    """修复 pyLDAvis 在新版 numpy 下的崩溃。

    numpy>=2 时 `np.linalg.eig` 对对称矩阵也会返回复数特征值，pyLDAvis 的
    PCoA 因此产出 complex128，保存 HTML 时报 "Object of type complex128 is
    not JSON serializable"。这里把 PCoA 换成专解对称矩阵的 eigh（结果为实数），
    并对负特征值截断到 0，其余算法完全一致。
    """
    try:
        import numpy as np
        from pyLDAvis import _prepare
    except ImportError:  # 未安装 pyLDAvis 时静默跳过，不影响分词/建模部分
        return
    if getattr(_prepare, "_numpy2_patched", False):
        return

    def _pcoa(pair_dists, n_components=2):
        pair_dists = np.asarray(pair_dists, np.float64)
        n = pair_dists.shape[0]
        h = np.eye(n) - np.ones((n, n)) / n
        b = -h.dot(pair_dists ** 2).dot(h) / 2
        eigvals, eigvecs = np.linalg.eigh(b)
        idx = eigvals.argsort()[::-1][:n_components]
        eigvals, eigvecs = np.clip(eigvals[idx], 0, None), eigvecs[:, idx]
        return eigvecs.dot(np.diag(np.sqrt(eigvals)))

    _prepare._pcoa = _pcoa
    _prepare._numpy2_patched = True


_patch_pyldavis_for_numpy2()
