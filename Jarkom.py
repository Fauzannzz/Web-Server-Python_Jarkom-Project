import socket

def tcp_server():
    SERVER_HOST = "127.0.0.1"  # Alamat IP untuk server
    SERVER_PORT = 6500  # Port untuk server

    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Membuat objek socket
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Mengatur opsi socket

    sock_server.bind((SERVER_HOST, SERVER_PORT))  # Mengikat socket ke alamat IP dan port tertentu

    sock_server.listen()  # Mendengarkan koneksi masuk

    print("Server ready.....")

    while True:
        sock_client, client_addres = sock_server.accept()  # Menerima koneksi dari client

        request = sock_client.recv(1024).decode()  # Menerima request dari client
        print("Dari client :" + request)

        response = handle_request(request)  # Menangani request dan menghasilkan response
        sock_client.send(response.encode())  # Mengirim response ke client

        sock_client.close()  # Menutup koneksi dengan client
    #endwhile
    sock_server.close()  # Menutup socket server


def handle_request(request):
    try:
        filename = request.split()[1][1:]  # Mendapatkan nama file yang diminta dari request
        with open(filename, 'r') as file:
            message_body = "<h1>HTTP/1.1 200 OK</h1>\n\n" + file.read()  # Membaca isi file
        response_line = "HTTP/1.1 200 OK\r\n"  # Baris pertama pada response
        print(response_line)
        content_type = "Content-Type: text/html\r\n\r\n"  # Tipe konten pada response
        response = response_line + content_type + message_body  # Menggabungkan semua bagian response
    except FileNotFoundError:
        response_line = "HTTP/1.1 404 Not Found\r\n"  # Baris pertama pada response
        print(response_line)
        content_type = "Content-Type: text/html\r\n\r\n"  # Tipe konten pada response
        message_body = "<h1>404 Not Found</h1><p>File tidak tersedia pada server.</p>"  # Isi pesan pada response
        response = response_line + content_type + message_body  # Menggabungkan semua bagian response

    return response

if __name__ == "__main__":
    tcp_server()  # Memulai server
