# prepare_model.py
import pandas as pd
import pickle
import re
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
stemmer = PorterStemmer()

csv_path = r"C:\Users\Swathi\OneDrive\Documents\music system\spotify_millsongdata.csv"
df = pd.read_csv(csv_path)
df = df[['song', 'text', 'artist']]
df['text'] = df['text'].fillna('')

def preprocess_text(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    stemmed_tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(stemmed_tokens)

df['processed_text'] = df['text'].apply(preprocess_text)

tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['processed_text'])

with open("fast_df.pkl", "wb") as f:
    pickle.dump(df, f)
with open("tfidf.pkl", "wb") as f:
    pickle.dump(tfidf, f)

print("✅ Pickle files created!")
