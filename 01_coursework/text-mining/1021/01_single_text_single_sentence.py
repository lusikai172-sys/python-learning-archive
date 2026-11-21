import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

from transformers import BertTokenizer, BertModel
import jieba

# ①单条文本单句子输入
# 第一步：分词
tokenizer = BertTokenizer.from_pretrained(str(BERT_MODEL_DIR))

text = '我爱自然语言处理'
tokenizer_output = tokenizer(text=text, return_tensors='pt')
print(tokenizer_output)
#
# 第二步：获取BERT词嵌入
model = BertModel.from_pretrained(str(BERT_MODEL_DIR))
outputs = model(input_ids=tokenizer_output['input_ids'],
                token_type_ids=tokenizer_output['token_type_ids'],
                attention_mask=tokenizer_output['attention_mask']
                            )

print(outputs.last_hidden_state.shape)
print(outputs.pooler_output.shape)

# print(outputs.last_hidden_state[0][0][:10])
# print(outputs.pooler_output[0][:10])

# print(outputs.last_hidden_state[0].max(dim=0)[:10])

max_val_dim0, max_index_dim0 = outputs.last_hidden_state[0].max(dim=0)
print(max_val_dim0[:10])
print(outputs.pooler_output[0][:10])





