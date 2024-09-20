import pandas as pd
import nltk
from nltk.data import find


def check_and_download_nltk_resources():
    try:
        find('corpora/stopwords.zip')
    except LookupError:
        nltk.download('stopwords')

    try:
        find('tokenizers/punkt.zip')
    except LookupError:
        nltk.download('punkt')


def read_quote_file(file_path):
    try:
        df = pd.read_excel(file_path)
        product_names = df.iloc[:, 0].tolist()
        return product_names

    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    except ValueError:
        print("Erro: O arquivo não pode ser lido como um arquivo Excel válido.")
    except IndexError:
        print("Erro: A planilha está vazia ou a coluna referenciada não existe.")
    except KeyError:
        print("Erro: A planilha 'Planilha1' não foi encontrada no arquivo Excel.")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def preprocess_text(text_list):
    preprocess_text_list = []
    try:
        check_and_download_nltk_resources()
        stop_words = set(nltk.corpus.stopwords.words('portuguese'))
        for text in text_list:
            words = nltk.word_tokenize(text.lower())
            words = [word for word in words if word not in stop_words]
            preprocess_text_list.append(' '.join(words))
        return preprocess_text_list

    except LookupError:
        print("Erro: Não foi possível encontrar os recursos necessários do NLTK (como stopwords ou tokenizer).")
    except TypeError:
        print("Erro: O texto fornecido não é válido. Verifique o tipo de dado que está passando.")
    except ValueError:
        print("Erro: Ocorreu um problema ao processar o texto. Verifique o conteúdo do texto.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
