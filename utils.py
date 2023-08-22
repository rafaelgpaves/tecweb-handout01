import os
import json

def extract_route(requisicao):

    comeco = requisicao.find("/") + 1
    rota = requisicao[comeco:]
    fim = rota.find(" ")
    return rota[:fim]

def read_file(path):

    with open(path, "rb") as f:
        return f.read()
    
def load_data(database):

    # with open(f"./data/{nome}") as f:
    #     data = json.load(f)

    # return data

    # adicionando suporte a database (handout 3):
    return database.get_all()

def load_template(arquivo):

    with open(f"templates/{arquivo}") as f:
        return f.read()
    
def build_response(body='', code=200, reason='OK', headers=''):

    return f"HTTP/1.1 {code} {reason}\n{headers}\n{body}".encode()