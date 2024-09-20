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
    try:
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        first_sheet_name = list(all_sheets.keys())[0]
        df = all_sheets[first_sheet_name]
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

    except FileNotFoundError as fnf_error:
        print(f"Erro: Arquivo não encontrado - {fnf_error}")
    except ValueError as ve:
        print(f"Erro de valor ao processar o arquivo ou treinar o modelo: {ve}")
    except KeyError as ke:
        print(f"Erro: Coluna ou planilha não encontrada - {ke}")
    except TypeError as te:
        print(f"Erro de tipo: {te}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def normalize_product(product_name_list, file_path):
    product_name_list_normalized = []
    try:
        product_name_list_processed = preprocess_text(product_name_list)
        model = joblib.load('files\\model.pkl')
        vectorizer = joblib.load('files\\vectorizer.pkl')
        label_encoder = joblib.load('files\\label_encoder.pkl')
        for product_name in product_name_list_processed:
            product_name_vectorized = vectorizer.transform([product_name])
            normalized_name_encoded = model.predict(product_name_vectorized)
            normalized_name = label_encoder.inverse_transform(normalized_name_encoded)
            product_name_list_normalized.append(normalized_name)
        df = pd.read_excel(file_path)
        while df.shape[1] < 2:
            df[df.shape[1]] = ""
        df[1] = pd.Series(str(item) for item in product_name_list_normalized)

        df.columns = ['Nome Produto', 'Produto Normalizado']
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=False, sheet_name='Produtos Normalizados')

        def normalize_item(item):
            if isinstance(item, list):
                return ', '.join(map(str, item))
            return str(item)
        return True


    except FileNotFoundError as fnf_error:
        print(f"Erro: Arquivo não encontrado - {fnf_error}")
        return False
    except ValueError as ve:
        print(f"Erro de valor ao vetorializar ou predizer: {ve}")
        return False
    except TypeError as te:
        print(f"Erro de tipo: {te}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False


def update_model(new_data, label):
    try:
        model = joblib.load('files\\model.pkl')
        vectorizer = joblib.load('files\\vectorizer.pkl')
        label_encoder = joblib.load('files\\label_encoder.pkl')
        new_data = preprocess_text(new_data)
        new_x = vectorizer.transform([new_data])
        new_y = label_encoder.transform([label])
        all_labels = list(label_encoder.classes_)
        y = label_encoder.fit_transform(all_labels)
        model.partial_fit(new_x, new_y, classes=np.unique(y))
        joblib.dump(model, 'files\\model.pkl')

    except FileNotFoundError as fnf_error:
        print(f"Erro: Arquivo não encontrado - {fnf_error}")
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except TypeError as te:
        print(f"Erro de tipo: {te}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
