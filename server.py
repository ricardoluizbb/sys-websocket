import asyncio
import websockets
import json
import datetime
from db import init_db, add_user, remove_user

connected_clients = set()

async def send_time():
    while True:
        current_time = datetime.datetime.now().isoformat()
        if connected_clients:
            tasks = [asyncio.create_task(client.send(current_time)) for client in connected_clients]
            await asyncio.gather(*tasks)
        await asyncio.sleep(1)

async def handle_client(websocket, path):
    user_id = str(websocket.remote_address)
    await add_user(user_id)
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if 'fibonacci' in data:
                n = int(data['fibonacci'])
                result = fibonacci(n)
                await websocket.send(json.dumps({"result": result}))
    finally:
        connected_clients.remove(websocket)
        await remove_user(user_id)

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

start_server = websockets.serve(handle_client, "localhost", 8000)

# Sobe as tabelas
loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())

# Métodos restantes
loop.run_until_complete(start_server)
loop.create_task(send_time())
loop.run_forever()
