import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from ModelProcessor import train_quote_model
from ModelProcessor import normalize_product
from Utils import read_quote_file


train_file_path = None
quote_file_path = None
model_update_file_path = None

def load_train_file():
    try:
        global train_file_path
        train_file_path = filedialog.askopenfilename(title="Selecione o arquivo para treinar modelo")
        if train_file_path:
            entry_train.delete(0, tk.END)
            entry_train.insert(0, train_file_path)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o arquivo de treino: {e}")


def load_quote_file():
    try:
        global quote_file_path
        quote_file_path = filedialog.askopenfilename(title="Selecione o arquivo para realizar cotação automática")
        if quote_file_path:
            entry_quote.delete(0, tk.END)
            entry_quote.insert(0, quote_file_path)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o arquivo de cotação: {e}")


def load_model_update_file():
    try:
        global model_update_file_path
        model_update_file_path = filedialog.askopenfilename(title="Selecione o arquivo para atualizar o modelo")
        if model_update_file_path:
            entry_update.delete(0, tk.END)
            entry_update.insert(0, model_update_file_path)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar o arquivo de atualização do modelo: {e}")


def save_train_files():
    try:
        train_files_save_path = filedialog.askopenfilename(title="Selecione a pasta para salvar os arquivos de treino")
        if train_files_save_path:
            entry_save_path.delete(0, tk.END)
            entry_save_path.insert(0, train_files_save_path)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os arquivos de treino: {e}")


def train_model():
    try:
        train_success = train_quote_model(train_file_path)
        if train_success:
            messagebox.showinfo("Treinar", "Treinamento realizado com sucesso!")
        else:
            messagebox.showinfo("Treinar", "Erro no treinamento!")

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de treino não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o treinamento do modelo: {e}")


def make_quote():
    try:
        normalized_name = normalize_product(read_quote_file(quote_file_path), quote_file_path)
        if normalized_name:
            messagebox.showinfo("Processando", "Cotação processada com sucesso!")
        else:
            messagebox.showinfo("Processando", "Erro no processamento!")

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de cotação não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento da cotação: {e}")


def update_model():
    try:
        messagebox.showinfo("Atualizar", "Modelo atualizado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante a atualização do modelo: {e}")


root = tk.Tk()
root.title("Aplicação WindowsForms")
root.geometry("980x230")

btn_load_train_file = tk.Button(root, text="Carregar arquivo para treino", command=load_train_file)
btn_load_train_file.grid(row=0, column=0, padx=10, pady=10)

btn_load_quote_file = tk.Button(root, text="Carregar arquivo para cotação", command=load_quote_file)
btn_load_quote_file.grid(row=0, column=1, padx=10, pady=10)

btn_load_update_model_file = tk.Button(root, text="Carregar arquivo para atualizar modelo",
                                       command=load_model_update_file)
btn_load_update_model_file.grid(row=0, column=2, padx=10, pady=10)

btn_train = tk.Button(root, text="Treinar", command=train_model)
btn_train.grid(row=1, column=0, padx=10, pady=10)

btn_process = tk.Button(root, text="Processar", command=make_quote)
btn_process.grid(row=1, column=1, padx=10, pady=10)

btn_update_model = tk.Button(root, text="Atualizar modelo", command=update_model)
btn_update_model.grid(row=1, column=2, padx=10, pady=10)

btn_update_model = tk.Button(root, text="Rota para salvar arquivos de treino:", command=save_train_files)
btn_update_model.grid(row=4, column=1, padx=10, pady=10)

entry_train = tk.Entry(root, width=50)
entry_train.grid(row=3, column=0, padx=10, pady=10)

entry_quote = tk.Entry(root, width=50)
entry_quote.grid(row=3, column=1, padx=10, pady=10)

entry_update = tk.Entry(root, width=50)
entry_update.grid(row=3, column=2, padx=10, pady=10)

entry_save_path = tk.Entry(root, width=100)
entry_save_path.grid(row=5, column=0, columnspan = 3, padx=10, pady=0)


root.mainloop()

# # Criar um ambiente virtual chamado 'venv'
# python -m venv venv
#
# # No Windows, ativar o ambiente virtual
# venv\Scripts\activate

# # No macOS/Linux, ativar o ambiente virtual
# source venv/bin/activate
#
# # Depois, instale os pacotes com:
# pip install -r requirements.txt