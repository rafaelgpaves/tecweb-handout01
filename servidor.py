import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index, delete, update, not_found
from database import Database

CUR_DIR = Path(__file__).parent

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

db = Database("getit")

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print('*'*100)
    print(request)

    route = extract_route(request)
    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request, database=db)
    elif "delete" in route.split("/"):
        response = delete(request, db, route[route.find("/")+1:route.find("?")])
        # response = index(request, db, True, route[route.find("/")+1:route.find("?")])
    elif "update" in route.split("/"):
        # response = delete(db, route[route.find("/")+1:route.find("?")])
        response = update(request, db, route[route.find("/")+1:route.find("?")], cancel="cancel" in route)
    else:
        response = not_found()

    client_connection.sendall(response)

    client_connection.close()

server_socket.close()