from cv2 import randShuffle
from datasets import load_dataset
import pandas as pd
from keybert import KeyBERT
from tqdm import tqdm


def clean(keywords):
    source_text = " ".join(map(str, keywords))
    return source_text

def clean_keywords(keywords):
  return clean(list(map(list, zip(*keywords)))[0])

def make_keywords(dataset):
  kw_model = KeyBERT()
  df = pd.DataFrame(columns=['text', 'keywords'])
  df["text"] = dataset["text"] 
  for i in tqdm(range(len(df))):
    keyword = kw_model.extract_keywords(df['text'][i])
    clean = clean_keywords(keyword)
    df["keywords"][i] = clean
  return df

def make_dataset(dataset="common_gen", split="train"):
    if dataset == "common_gen":
        dataset = load_dataset(dataset, split=split)
        df = pd.DataFrame()
        df["keywords"] = dataset["concepts"]
        df["text"] = dataset["target"]
        df["keywords"] = df["keywords"].apply(clean)
        return df
    else:
        dataset = load_dataset(dataset, split=split)
        print(dataset)
        df = make_keywords(dataset=dataset)
        return df
  