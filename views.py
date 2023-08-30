from utils import load_data, load_template
from urllib.parse import unquote_plus
import json
from utils import build_response
from database import Note

def index(request, database, delete=False, delete_id=None):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    # if delete and str(delete_id).isnumeric():
    #     database.delete(delete_id)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus
        for chave_valor in corpo.split('&'):
            print(chave_valor)
            # AQUI É COM VOCÊ
            chave = chave_valor.split("=")[0]
            valor = unquote_plus(chave_valor.split("=")[1])
            params[chave] = valor
        add_to_json(database, params)
        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de <li>'s para cada anotação
    # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=dados.id, title=dados.title, details=dados.content)
        for dados in load_data(database=database)
    ]
    notes = '\n'.join(notes_li)

    return build_response() + load_template('index.html').format(notes=notes).encode()

def delete(request, database, id):

    if delete and str(id).isnumeric():
        database.delete(id)
    
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=dados.id, title=dados.title, details=dados.content)
        for dados in load_data(database=database)
    ]
    notes = '\n'.join(notes_li)

    return build_response() + load_template('index.html').format(notes=notes).encode()

def update(request, database, id, cancel=False):

    if request.startswith('POST'):

        if not cancel:
            request = request.replace('\r', '')  # Remove caracteres indesejados
            partes = request.split('\n\n')
            corpo = partes[1]
            params = {}
            for chave_valor in corpo.split('&'):
                chave = chave_valor.split("=")[0]
                valor = unquote_plus(chave_valor.split("=")[1])
                params[chave] = valor
            database.update(Note(id=id, title=params["title"], content=params["content"]))

        note_template = load_template('components/note.html')
        notes_li = [
            note_template.format(id=dados.id, title=dados.title, details=dados.content)
            for dados in load_data(database=database)
        ]
        notes = '\n'.join(notes_li)
        return build_response() + load_template('index.html').format(notes=notes).encode()

    return build_response() + load_template("update.html").format(title=database.get_id(id).title, content=database.get_id(id).content).encode()

def not_found():
    return build_response() + load_template("notfound.html").encode()

def add_to_json(database, anotacao):

    # with open("./data/notes.json") as f:
    #     data = json.load(f)
    #     data.append(anotacao)

    # with open("./data/notes.json", "w") as f:
    #     json.dump(data, f)

    # adicionando suporte a database (handout 3):
    database.add(Note(title=anotacao["titulo"], content=anotacao["detalhes"]))