import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

from transformers import BertTokenizer, BertModel

'''
两条文本
我，爱，自然语言处理  （token数为3）
我，爱，吃，苹果    （token数为4）

经过补长过后，变成：
我，爱，自然语言处理，<pad>    （token数为4）
我，爱，吃，苹果    （token数为4）

'''


# ③多条文本单句子输入
tokenizer = BertTokenizer.from_pretrained(str(BERT_MODEL_DIR))
texts = ['我爱自然语言处理', '我爱吃苹果']
tokenizer_output = tokenizer(text=texts, return_tensors='pt', padding=True)
print(tokenizer_output)
# input_ids : 101表示[cls]， 102表示[sep]， 0表示[pad]
# attention_mask:0表示[pad]
# [pad]不应该作为计算权重的一部分，应该遮蔽

# 第二步：获取BERT词嵌入
model = BertModel.from_pretrained(str(BERT_MODEL_DIR))
outputs = model(input_ids=tokenizer_output['input_ids'], attention_mask=tokenizer_output['attention_mask'],
                            token_type_ids=tokenizer_output['token_type_ids'])

print(outputs.last_hidden_state.shape) #
print(outputs.pooler_output.shape)

# 取第二个句子的【cls】向量
# print(outputs.last_hidden_state[1][0])