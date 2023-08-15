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