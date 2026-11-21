import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

from transformers import BertTokenizer, BertModel

# ②单条文本双句子输入
# 第一步：分词
tokenizer = BertTokenizer.from_pretrained(str(BERT_MODEL_DIR))
text = '我爱自然语言处理'
text2 = '我觉得学习自然语言处理未来我能用得上'
tokenizer_output = tokenizer(text=text, text_pair=text2, return_tensors='pt')
print(tokenizer_output)

# 第二步：获取BERT词嵌入
model = BertModel.from_pretrained(str(BERT_MODEL_DIR))
outputs = model(input_ids=tokenizer_output['input_ids'], attention_mask=tokenizer_output['attention_mask'],
                            token_type_ids=tokenizer_output['token_type_ids'])

print(outputs.last_hidden_state.shape)
print(outputs.pooler_output.shape)
