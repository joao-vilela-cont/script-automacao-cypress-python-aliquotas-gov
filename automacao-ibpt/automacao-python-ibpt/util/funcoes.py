import json
import os
import zipfile
from datetime import datetime
from types import SimpleNamespace
from repositories.connectionMongo import save_ibpt
from util.constants import*

def start(argEnvironment):
    lista_arquivos_csvs = []
    arquivos = get_arquivos()
    if arquivos:
        for arquivo in arquivos:
            if arquivo.endswith('.csv'):
                lista_arquivos_csvs.append(arquivo)
        valores_csv_to_json(lista_arquivos_csvs, argEnvironment)

def valores_csv_to_json(arquivos, argEnvironment):
    lista_dados_csv = []
    for arquivo in arquivos:
        caminho_arquivo_csv = os.path.join(PASTA_ORIGEM, arquivo)
        with open(caminho_arquivo_csv, 'r', encoding='Windows-1252') as file:
            next(file)
            for linha in file:
                dados_por_linha = (linha.split(';'))
                dados_por_linha.append(get_uf(arquivo))
                lista_dados_csv.append(dados_por_linha)
    save_ibpt(json.loads(build_json(lista_dados_csv)), getEnvironment(argEnvironment))
    remover_arquivos_extraidos(PASTA_ORIGEM)

def build_json(lista):
    objects = [] 
    for atributo in lista:
        dados_json = {
            "_id": {
                "ncm": format_codigo(atributo[0]),
                "ex": atributo[1],
                "uf": atributo[13]
            },
            "nacional": atributo[4],
            "estadutal": atributo[6],
            "importado": atributo[5],
            "municipal": atributo[7],
            "vigenciaInicio": converter_data(atributo[8]),
            "vigenciaFim": converter_data(atributo[9]),
            "versao": atributo[11],
        }
        objects.append(dados_json)
    return json.dumps(objects, indent=4, default=json_serial)

def get_arquivos():
    arquivos_zip = [f for f in os.listdir(PASTA_ORIGEM) if f.endswith('.zip')]
    arquivos_zip_recente = sorted(arquivos_zip, key=lambda x: os.path.getctime(os.path.join(PASTA_ORIGEM, x)), reverse=True)
    if arquivos_zip:
        zip_file = zipfile.ZipFile(os.path.join(PASTA_ORIGEM, arquivos_zip_recente[0]), 'r')
        lista_arquivos = zip_file.namelist()
        zip_file.extractall(PASTA_ORIGEM)
        zip_file.close()
        return lista_arquivos
    else:
        return []

def remover_arquivos_extraidos(diretorio):
    for arquivo in os.listdir(diretorio):
        if not arquivo.endswith(".zip"):
            caminho_completo = os.path.join(diretorio, arquivo)
            os.remove(caminho_completo)

def get_uf(nome_arquivo):
    posicao_ibptax = nome_arquivo.find("IBPTax")
    return nome_arquivo[posicao_ibptax + 6:posicao_ibptax + 8]

def format_codigo(string):
    if string[0] == '0':
        if string[1] == '0':
            return '0'
        else:
            return string[1:]
    else:
        return string

def converter_data(data_str_br):
    return datetime.strptime(data_str_br, '%d/%m/%Y')

def converter_data(data_str_br):
    return datetime.strptime(data_str_br, "%d/%m/%Y")

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Tipo de objeto não serializável")

def getEnvironment(argEnvironment):
    json_file = open('config/environments.json', 'r')
    data = json.load(json_file)
    json_file.close()
    if argEnvironment in data:
        return SimpleNamespace(**data[argEnvironment])
    else:
        return None