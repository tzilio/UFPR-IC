import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json

def carregar_json(caminho_json):
    try:
        with open(caminho_json, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showwarning("Erro", f"Arquivo JSON não encontrado: {caminho_json}")
        return None

def salvar_json(dados, caminho_json):
    with open(caminho_json, 'w') as f:
        json.dump(dados, f, indent=4)

def atualizar_imagem():
    global img_index
    while img_index < len(dados_imagens):
        dados_json = dados_imagens[img_index]

        if (modo_selecionado.get() == "Anotar" and dados_json['anotador'] == usuario and not dados_json.get('placa_anotada')) or \
           (modo_selecionado.get() == "Validar" and dados_json['validador'] == usuario and not dados_json.get('placa_validada')):
            
            caminho_imagem = os.path.join(diretorio_imagens, dados_json['nome'])
            if os.path.exists(caminho_imagem):
                img = Image.open(caminho_imagem)
                img = img.resize((400, 300), Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                label_img.config(image=tk_img)
                label_img.image = tk_img
                label_info.config(text=f"Imagem {img_index + 1}/{len(dados_imagens)}")

                if modo_selecionado.get() == "Anotar":
                    label_placa_default.config(text=f"Placa Default: {dados_json['placa_default']}")
                    entrada_placa.delete(0, tk.END)
                    entrada_placa.insert(0, dados_json.get('placa_anotada', ''))

                elif modo_selecionado.get() == "Validar":
                    label_placa_default.config(text=f"Placa Anotada: {dados_json.get('placa_anotada', 'Não anotada')}")
                    entrada_placa.delete(0, tk.END)
                    entrada_placa.insert(0, dados_json.get('placa_validada', ''))

                var_invalida.set(dados_json.get('invalida', False))
                break
            else:
                messagebox.showwarning("Erro", f"Imagem não encontrada: {caminho_imagem}")
                img_index += 1
        else:
            img_index += 1

    else:
        messagebox.showinfo("Fim", "Todas as imagens foram verificadas!")
        root.quit()

def verificar_mercosul(placa):
    if len(placa) >= 5:
        return placa[4].isalpha()
    return False

def salvar_decisao():
    global img_index
    dados_json = dados_imagens[img_index]

    if dados_json:
        placa_inserida = entrada_placa.get().strip()

        if modo_selecionado.get() == "Anotar":
            if not placa_inserida:
                dados_json['placa_anotada'] = dados_json['placa_default']
            else:
                dados_json['placa_anotada'] = placa_inserida

            dados_json['mercosul'] = verificar_mercosul(dados_json['placa_anotada'])
            dados_json['invalida'] = var_invalida.get()

        elif modo_selecionado.get() == "Validar":
            if not placa_inserida:
                dados_json['placa_validada'] = dados_json.get('placa_anotada', "")
            else:
                dados_json['placa_validada'] = placa_inserida

            dados_json['mercosul'] = verificar_mercosul(dados_json['placa_validada'])
            dados_json['invalida'] = var_invalida.get()

        salvar_json(dados_imagens, caminho_json)
    
    img_index += 1
    atualizar_imagem()

def iniciar_processamento():
    global diretorio_imagens, dados_imagens, img_index, usuario, caminho_json

    usuario = entrada_usuario.get()
    modo = modo_selecionado.get()

    if not usuario:
        messagebox.showwarning("Erro", "Por favor, insira o nome do usuário.")
        return

    diretorio_imagens = filedialog.askdirectory(title="Selecione a pasta com as imagens (ex.: IMAGES)")
    if not diretorio_imagens:
        return

    caminho_json = filedialog.askopenfilename(title="Selecione o arquivo JSON (ex.: dados_imagens.json)", filetypes=[("JSON files", "*.json")])
    if not caminho_json:
        return

    dados_imagens = carregar_json(caminho_json)

    if not dados_imagens:
        messagebox.showwarning("Erro", "Nenhum dado encontrado no arquivo JSON.")
        return

    img_index = 0
    atualizar_imagem()

# GUI
root = tk.Tk()
root.title("Anotar/Validar Placas de Veículos")

label_modo = tk.Label(root, text="Selecione o Modo:")
label_modo.pack(pady=5)

modo_selecionado = tk.StringVar()
modo_selecionado.set("Anotar") 

radio_anotar = tk.Radiobutton(root, text="Anotar", variable=modo_selecionado, value="Anotar")
radio_anotar.pack()

radio_validar = tk.Radiobutton(root, text="Validar", variable=modo_selecionado, value="Validar")
radio_validar.pack()

label_usuario = tk.Label(root, text="Nome do Usuário:")
label_usuario.pack(pady=5)

entrada_usuario = tk.Entry(root)
entrada_usuario.pack(pady=5)

btn_iniciar = tk.Button(root, text="Iniciar", command=iniciar_processamento)
btn_iniciar.pack(pady=10)

label_img = tk.Label(root)
label_img.pack(pady=20)

label_info = tk.Label(root, text="Imagem 0/0")
label_info.pack()

label_placa_default = tk.Label(root, text="Placa Default: ")
label_placa_default.pack()

frame_placa = tk.Frame(root)
frame_placa.pack(pady=10)

label_placa = tk.Label(frame_placa, text="Placa:")
label_placa.grid(row=0, column=0)

entrada_placa = tk.Entry(frame_placa)
entrada_placa.grid(row=0, column=1)

# Remover checkbox para Mercosul (já removido)

# Checkbox para Placa Inválida
var_invalida = tk.BooleanVar()
check_invalida = tk.Checkbutton(root, text="Placa Inválida", variable=var_invalida)
check_invalida.pack(pady=5)

# Remover checkbox para Placa Correta (já removido)

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

btn_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar_decisao)
btn_salvar.grid(row=0, column=0, padx=10)

root.mainloop()
