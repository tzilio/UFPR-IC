import os
import json
import random
from collections import defaultdict

participantes = ["Thiago", "Rafael", "Leonardo"]

def escolher_participante(contagem_participantes, excluir=None):
    candidatos = [p for p in participantes if p != excluir]
    
    min_valor = min(contagem_participantes[p] for p in candidatos)
    candidatos_com_menos_atribuicoes = [p for p in candidatos if contagem_participantes[p] == min_valor]
    
    escolhido = random.choice(candidatos_com_menos_atribuicoes)
    contagem_participantes[escolhido] += 1
    return escolhido

def extrair_placa(nome_arquivo):
    try:
        placa = nome_arquivo.split('-')[1]
        return placa
    except IndexError:
        return None

def criar_json_para_imagem(diretorio):
    contagem_anotadores = defaultdict(int, {p: 0 for p in participantes})
    contagem_validadores = defaultdict(int, {p: 0 for p in participantes})

    dados_imagens = []

    for arquivo in os.listdir(diretorio):
        if os.path.isfile(os.path.join(diretorio, arquivo)) and arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            placa_default = extrair_placa(arquivo)

            if placa_default is None:
                mercosul = False
                invalida = True
            else:
                mercosul = placa_default[4].isalpha() if len(placa_default) > 4 else False
                invalida = False

            anotador = escolher_participante(contagem_anotadores)
            validador = escolher_participante(contagem_validadores, excluir=anotador)

            dados_imagem = {
                "nome": arquivo,
                "placa_default": placa_default if placa_default else "",
                "placa_anotada": "",
                "placa_validada": "",
                "anotador": anotador,
                "validador": validador,
                "mercosul": mercosul,
                "invalida": invalida
            }

            dados_imagens.append(dados_imagem)

    nome_json = 'dados_imagens.json'
    caminho_json = os.path.join(diretorio, nome_json)

    with open(caminho_json, 'w') as f:
        json.dump(dados_imagens, f, indent=4)

    print(f"Arquivo JSON criado: {caminho_json}")

diretorio = './IMAGES'
criar_json_para_imagem(diretorio)
