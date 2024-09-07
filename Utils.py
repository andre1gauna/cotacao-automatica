import pandas as pd
import nltk

def read_quote_file(file_path):
    df = pd.read_excel(file_path, sheet_name='Planilha1')
    product_names = df.iloc[:, 0].tolist()
    return product_names[0]

def preprocess_text(text):
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    stop_words = set(nltk.corpus.stopwords.words('portuguese'))
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)