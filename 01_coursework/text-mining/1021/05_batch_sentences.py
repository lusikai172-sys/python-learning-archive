import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import BERT_MODEL_DIR, TEXT_DATA_DIR  # noqa: E402

from transformers import BertTokenizer, BertModel

with open(f'{TEXT_DATA_DIR}/第四章/深度学习评论.txt', 'r', encoding='utf-8') as f:
    texts = [i.strip() for i in f.readlines()]


tokenizer = BertTokenizer.from_pretrained(str(BERT_MODEL_DIR))
tokenizer_output = tokenizer(text=texts, return_tensors='pt', padding=True)
print(tokenizer_output)


model = BertModel.from_pretrained(str(BERT_MODEL_DIR))
outputs = model(input_ids=tokenizer_output['input_ids'], attention_mask=tokenizer_output['attention_mask'],
                            token_type_ids=tokenizer_output['token_type_ids'])

print(outputs.last_hidden_state.shape)
print(outputs.pooler_output.shape)

