import torch
import torch_xla.core.xla_model as xm
from keytotext import trainer, make_dataset
import pandas as pd

train_df1 = make_dataset('common_gen', split='train')
train_df2 = make_dataset("ag_news", split="train")
train_df3 = make_dataset("cc_news", split="train")
train_df = pd.concat([train_df1, train_df2, train_df3])
eval_df = make_dataset('common_gen', split='validation')
test_df = make_dataset('common_gen', split='test')


model = trainer()
model.from_pretrained(model_name="t5-base")
model.train(train_df=train_df, test_df=eval_df, batch_size=4, max_epochs=10, use_gpu=False,tpu_cores=8)
print(model.evaluate(test_df=test_df))
model.upload(hf_username="gagan3012", model_name="k2tt5")
