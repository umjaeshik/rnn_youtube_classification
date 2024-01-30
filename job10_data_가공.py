import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model
import datetime

df = pd.read_csv('./data/result_youtube_20240130.csv')
print(df.head())
result = pd.DataFrame()

result = df[df['OX']=='X']
result.to_csv('./predict_data/result_X.csv',index=False)
