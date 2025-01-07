
!pip install --no-index --find-links=. transformers
!pip install --no-index --find-links=. datasets
model_nm = "microsoft/deberta-v3-small"

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments,Trainer
from pathlib import Path
from datasets import Dataset,DatasetDict
import datasets
path = Path('/kaggle/input/us-patent-phrase-to-phrase-matching')
mypath = Path('/kaggle/input/us-patents-libraries-model-tokenizer')

import pandas as pd

# tokenizer
chosen_pretrained_model = "microsoft/deberta-v3-small"

# og
debv3_tokenizer = AutoTokenizer.from_pretrained(mypath)
model = AutoModelForSequenceClassification.from_pretrained(mypath)


# path
path = Path('/kaggle/input/us-patent-phrase-to-phrase-matching') # Using GUI places comp-data into 'kaggle/input' folder

# pandas dataframe
df = pd.read_csv(path/'train.csv')
df['input'] = 'TEXT1: ' + df.context + '; TEXT2: ' + df.target + '; ANC1: ' + df.anchor

# huggingface datasets
hf_datasets = Dataset.from_pandas(df)

def tok_func(x): return debv3_tokenizer(x["input"])
tok_ds = hf_datasets.map(tok_func, batched=True)

tok_ds = tok_ds.rename_columns({'score':'labels'})
tok_ds_dicts = tok_ds.train_test_split(0.25, seed=42)

# training
bs = 128
epochs = 4
lr = 8e-5

args = TrainingArguments('outputs', learning_rate=lr, warmup_ratio=0.1, lr_scheduler_type='cosine', fp16=True,
    evaluation_strategy="epoch", per_device_train_batch_size=bs, per_device_eval_batch_size=bs*2,
    num_train_epochs=epochs, weight_decay=0.01, report_to='none')

import numpy as np
def corr(x,y): return np.corrcoef(x,y)[0][1]
def corr_d(eval_pred): return {'pearson': corr(*eval_pred)}

trainer = Trainer(model, 
                  args, 
                  train_dataset=tok_ds_dicts['train'], 
                  eval_dataset=tok_ds_dicts['test'],
                  tokenizer=debv3_tokenizer, 
                  compute_metrics=corr_d)

trainer.train()

eval_df = pd.read_csv(path/'test.csv')
eval_df['input'] = 'TEXT1: ' + eval_df.context + '; TEXT2: ' + eval_df.target + '; ANC1: ' + eval_df.anchor
eval_ds = Dataset.from_pandas(eval_df).map(tok_func, batched=True)

preds = trainer.predict(eval_ds).predictions.astype(float)
preds = np.clip(preds, 0, 1)


submission = datasets.Dataset.from_dict({
    'id': eval_ds['id'],
    'score': preds.squeeze()
})

submission.to_csv('submission.csv', index=False)