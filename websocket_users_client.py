import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            message = "Привет, сервер!"
            print(f"Подключено к серверу: {uri}")
            print(f"Отправлено серверу: {message}")
            await websocket.send(message)

            # Получаем 5 сообщений
            for i in range(5):
                response = await websocket.recv()
                print(f"Сообщение от сервера [{i+1}]: {response}")

    except Exception as e:
        print(f"Ошибка при приёме сообщения: {e}")

if __name__ == "__main__":
    asyncio.run(client())
