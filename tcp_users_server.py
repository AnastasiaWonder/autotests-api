import socket

# Список всех сообщений
messages = []


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(10)

    print("TCP сервер запущен на localhost:12345")
    print("Ожидание подключений...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Пользователь с адресом: {client_address} подключился к серверу")

        # Принимаем сообщение
        data = client_socket.recv(1024).decode()

        print(f"Пользователь с адресом: {client_address} отправил сообщение: {data}")

        # Сохраняем в историю
        messages.append(data)

        # Формируем ответ — всю историю, каждое сообщение с новой строки
        history = "\n".join(messages)

        client_socket.send(history.encode())

        client_socket.close()


if __name__ == '__main__':
    server()
