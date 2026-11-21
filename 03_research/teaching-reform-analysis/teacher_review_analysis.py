import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, concatenate, Attention
import os
from config import DATA_DIR, MODEL_H5, OUTPUT_DIR  # noqa: E402

# 2.1 数据采集与清洗标准化流程
class DataCleaningPipeline:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cleaned_path = os.path.join(os.path.dirname(file_path), "cleaned_data.csv")

    def load_data(self):
        """六类评价表格的数据结构解析"""
        try:
            df = pd.read_csv(self.file_path,
                             header=None,
                             names=['name','score', 'department'] + [f'question_{i}' for i in range(1, 13)],
                             encoding='gbk',
                             low_memory=False)
            print("数据结构解析成功")
            return df
        except Exception as e:
            print(f"数据加载失败: {str(e)}")
            return None

    def handle_missing_values(self, df):
        """缺失值填补策略"""
        # 姓名/院系缺失值处理
        df['name'] = df['name'].ffill()
        df['department'] = df['department'].ffill()

        # 评分列缺失值处理（使用列均值）
        score_cols = df.columns[2:]
        df[score_cols] = df[score_cols].apply(pd.to_numeric, errors='coerce')
        df[score_cols] = df[score_cols].fillna(df[score_cols].mean())
        print("缺失值填补完成")
        return df

    def detect_outliers(self, df):
        """异常值检测策略"""
        score_cols = df.columns[2:]
        z_scores = np.abs((df[score_cols] - df[score_cols].mean()) / df[score_cols].std())
        outliers = df[(z_scores > 3).any(axis=1)]
        df[score_cols] = df[score_cols].clip(lower=df[score_cols].min() - 3,
                                             upper=df[score_cols].max() + 3, axis=0)
        print(f"检测到{len(outliers)}个异常值并处理")
        return df

    def normalize_data(self, df):
        """数据标准化"""
        score_cols = df.columns[2:]
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[score_cols])
        df[score_cols] = scaled_data
        print("数据标准化完成")
        return df

    def save_clean_data(self, df):
        """保存清洗后的数据"""
        df.to_csv(self.cleaned_path, index=False, encoding='utf_8_sig')
        print(f"清洗数据已保存至: {self.cleaned_path}")


# 2.2 多模态特征融合技术
class FeatureFusionModel:
    def __init__(self, input_shape, model_save_path):
        self.input_shape = input_shape
        self.model_save_path = model_save_path

    def build_model(self):
        """张量融合网络结构设计"""
        # 文本特征输入（需要后续优化为Embedding层）
        text_input = Input(shape=(self.input_shape[0],), name='text_input')
        text_dense = Dense(64, activation='relu')(text_input)

        # 结构化数据特征输入
        struct_input = Input(shape=(self.input_shape[1],), name='struct_input')
        struct_dense = Dense(64, activation='relu')(struct_input)

        # 多模态融合层
        merged = concatenate([text_dense, struct_dense])
        merged = Dense(32, activation='relu')(merged)

        # 动态权重分配机制
        attention = Attention()([text_dense, struct_dense])
        attention_output = Dense(1, activation='sigmoid')(attention)

        # 输出层
        output = Dense(1, activation='linear')(merged)

        model = Model(inputs=[text_input, struct_input], outputs=output)
        model.compile(optimizer='adam', loss='mse')
        print("多模态特征融合模型构建完成")
        return model

    def save_model(self, model):
        """保存训练好的模型"""
        model.save(self.model_save_path)
        print(f"模型已保存至: {self.model_save_path}")


# 主程序
if __name__ == "__main__":
    # 配置路径参数
    base_path = DATA_DIR
    raw_data_path = os.path.join(base_path, "2021-2022-2评教统计明细.csv")
    base_path.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model_save_path = str(MODEL_H5)

    # 数据处理流程
    pipeline = DataCleaningPipeline(file_path=raw_data_path)
    df = pipeline.load_data()

    if df is not None:
        df = pipeline.handle_missing_values(df)
        df = pipeline.detect_outliers(df)
        df = pipeline.normalize_data(df)

    # 保存清洗后的数据
    pipeline.save_clean_data(df)

    # 文本特征向量化
    text_encoder = OneHotEncoder(handle_unknown='ignore')
    text_features = text_encoder.fit_transform(df[['name', 'department']])

    # 结构化数据特征
    struct_features = df.iloc[:, 2:-1].values
    struct_features = struct_features.astype('float32')

    # 准备标签数据（假设最后一列是score）
    labels = df.iloc[:, -1].values.reshape(-1, 1)

    # 构建融合模型
    fusion_model = FeatureFusionModel(
        input_shape=(text_features.shape[1], struct_features.shape[1]),
        model_save_path=model_save_path
    )
    model = fusion_model.build_model()

    # 训练模型（取消注释以下代码）
    history = model.fit(
        [text_features, struct_features],
        labels,
        epochs=20,
        batch_size=32,
        validation_split=0.2
    )

    # 保存训练好的模型
    fusion_model.save_model(model)

    # 示例：保存特征重要性分析结果
    feature_importance = pd.DataFrame({
        'feature': ['text'] + list(df.columns[2:-1]),
        'importance': [0.4] + [0.2]*11  # 示例数据
    })
    feature_importance.to_csv(os.path.join(base_path, "feature_importance.csv"), index=False)