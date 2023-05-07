import socket

def tcp_server():
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 65000

    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock_server.bind((SERVER_HOST, SERVER_PORT))

    sock_server.listen()

    print("Server ready.....")

    while True:
        sock_client, client_addres = sock_server.accept()

        request = sock_client.recv(1024).decode()
        print("Dari client :"+request)

        response = handle_request(request)
        sock_client.send(response.encode())

        sock_client.close()
    #endwhile
    sock_server.close()


def handle_request(request):
    try:
        filename = request.split()[1][1:]
        with open(filename, 'r') as file:
            message_body = file.read()
        response_line = "HTTP/1.1 200 OK\r\n"
        content_type = "Content-Type: text/html\r\n\r\n"
        response = response_line+content_type+message_body
    except FileNotFoundError:
        response_line = "HTTP/1.1 404 Not Found\r\n"
        content_type = "Content-Type: text/html\r\n\r\n"
        message_body = "<h1>404 Not Found</h1><p>File tidak tersedia pada server.</p>"
        response = response_line+content_type+message_body

    return response

if __name__ == "__main__":
    tcp_server()
 
