import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

from transformers import BertTokenizer, BertModel
from tqdm import tqdm

with open(f'{TEXT_DATA_DIR}/第四章/深度学习评论.txt', 'r', encoding='utf-8') as f:
    texts = [i.strip() for i in f.readlines()]

tokenizer = BertTokenizer.from_pretrained(str(BERT_MODEL_DIR))
model = BertModel.from_pretrained(str(BERT_MODEL_DIR))

# # 获得每个词的向量表示
# result_list = []
# for i in tqdm(texts):
#     tokenizer_output = tokenizer(text=i, return_tensors='pt')
#     outputs = model(
#         input_ids=tokenizer_output['input_ids'],
#         attention_mask=tokenizer_output['attention_mask'],
#         token_type_ids=tokenizer_output['token_type_ids'])
#     print(outputs.last_hidden_state.shape)
#     result_list.append(outputs.last_hidden_state.squeeze(0))
# #
# #
# from torch.nn.utils.rnn import pad_sequence
# output_all = pad_sequence(result_list, batch_first=True)
# print(output_all.shape)

# # 获得每个句子的向量表示①自己实现
# result_list = []
# for i in tqdm(texts):
#     tokenizer_output = tokenizer(text=i, return_tensors='pt')
#     outputs = model(
#         input_ids=tokenizer_output['input_ids'],
#         attention_mask=tokenizer_output['attention_mask'],
#         token_type_ids=tokenizer_output['token_type_ids'])
#     print(outputs.pooler_output.shape)
#     result_list.append(outputs.pooler_output) # 原来的元素
#
# import torch
# output_all = torch.cat(result_list, dim=0)
# print(output_all.shape)

# 获得每个句子的向量表示②使用transfomer.pipeline
from transformers.pipelines import pipeline
embedding_model = pipeline(
    task='feature-extraction',
    model=str(BERT_MODEL_DIR)
)
output = embedding_model(texts) # 注意，这里的output格式为list
#
sentence_vectors = []
print(output)
for i in output:
    print(len(i[0][0]))
    sentence_vectors.append(i[0][0])

#
# # 获得每个句子每个词的向量表示，并补长、合并
# # 第一步：获取每个句子的每个词的向量表示，并转化为list[torch.tensor]格式
# import torch
# sentence_word_embeddings = [torch.tensor(i[0], dtype=torch.float32) for i in output]
# # 第二步：补长与合并
# from torch.nn.utils.rnn import pad_sequence
# output_all = pad_sequence(sentence_word_embeddings, batch_first=True)
# print(output_all.shape)
#
# # 获得每个句子的向量表示，并合并
# import torch
# # 第一步：获取每个句子的向量表示，并转化为list[torch.tensor]格式
# sentence_embeddings = [torch.tensor(i[0][0], dtype=torch.float32) for i in output]
# # 第二步：合并
# output_all = torch.stack(sentence_embeddings)
# print(output_all.shape)
#
