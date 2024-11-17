import asyncio
import websockets
import json

async def test_websocket():
    #  Замените <ваш JWT токен> на реальный токен, полученный через систему авторизации
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNDI3MjAzLCJpYXQiOjE3MzA5OTUyMDMsImp0aSI6ImUyMTllYzdiNDgzMjRkMGU5M2RmOTQxYmRiMTBmNTUwIiwidXNlcl9pZCI6M30.XQ7YsdpqlBuloUQtzyTGBaYzJOxRDDRmCZEgAxAtn4E"
    uri = f"ws://127.0.0.1:8000/ws/chat/prosto/?token={token}"

    async with websockets.connect(uri) as websocket:
        #  Отправка тестового сообщения на сервер
        message = {"message": "Привет от WebSocket клиента!"}
        await websocket.send(json.dumps(message))

        response = await websocket.recv()
        print("Получено сообщение:", response)

asyncio.run(test_websocket())
