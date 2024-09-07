import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import joblib
from Utils import preprocess_text

def train_quote_model(file_path):
    df = pd.read_excel(file_path, sheet_name='Planilha1')
    product_names = df.iloc[:, 0].tolist()
    normalized_names = df.iloc[:, 1].tolist()
    data = {'produto_variacao': product_names, 'produto_normalizado': normalized_names}
    df = pd.DataFrame(data)
    df['produto_variacao'] = df['produto_variacao'].apply(preprocess_text)

    vectorizer = TfidfVectorizer()
    label_encoder = LabelEncoder()
    x = vectorizer.fit_transform(df['produto_variacao'])
    y = label_encoder.fit_transform(df['produto_normalizado'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = SGDClassifier(loss='log_loss', warm_start=True, learning_rate='constant', eta0=0.01)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Acurácia no conjunto de teste: {accuracy:.2f}')

    joblib.dump(model, 'files\\model.pkl')
    joblib.dump(vectorizer, 'files\\vectorizer.pkl')
    joblib.dump(label_encoder, 'files\\label_encoder.pkl')


def normalize_product(product_name):
    product_name = preprocess_text(product_name)
    model = joblib.load('files\\model.pkl')
    vectorizer = joblib.load('files\\vectorizer.pkl')
    label_encoder = joblib.load('files\\label_encoder.pkl')
    product_name_vectorized = vectorizer.transform([product_name])
    normalized_name_encoded = model.predict(product_name_vectorized)
    normalized_name = label_encoder.inverse_transform(normalized_name_encoded)
    return normalized_name[0]


def update_model(new_data, label):
    model = joblib.load('files\\model.pkl')
    vectorizer = joblib.load('files\\vectorizer.pkl')
    label_encoder = joblib.load('files\\label_encoder.pkl')
    new_data = preprocess_text(new_data)
    new_x = vectorizer.transform([new_data])
    new_y = label_encoder.transform([label])
    all_labels = list(label_encoder.classes_)
    y = label_encoder.fit_transform(all_labels)
    model.partial_fit(new_x, new_y, classes=np.unique(y))
    joblib.dump(model, 'model.pkl')
