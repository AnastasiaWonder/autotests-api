import asyncio
import websockets

# Обработчик соединения
async def handler(websocket):
    try:
        # Получаем одно сообщение от клиента
        message = await websocket.recv()
        print(f"Получено сообщение от пользователя: {message}")

        # Отправляем 5 ответных сообщений
        for i in range(1, 6):
            response = f"{i} Сообщение пользователя: {message}"
            await websocket.send(response)
            await asyncio.sleep(0.05)  # короткая пауза, чтобы не упало

    except websockets.exceptions.ConnectionClosedOK:
        print("Соединение закрыто клиентом")
    except Exception as e:
        print(f"Ошибка на сервере: {e}")

async def main():
    # Создаем сервер
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket сервер запущен на ws://localhost:8765")
        await asyncio.Future()  # держим сервер в рабочем состоянии

if __name__ == "__main__":
    asyncio.run(main())
