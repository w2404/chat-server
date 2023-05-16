import asyncio
import websockets

# WebSocket 服务器的主机和端口
host = 'localhost'
port = 8000

# WebSocket 连接的路径
websocket_path = '/api'

# 处理接收到的消息
async def handle_message(message):
    print(f'Received message: {message}')

# 发送消息到服务器
async def send_message(websocket):
    while True:
        message = input('Enter message (or q to quit): ')
        if message == 'q':
            break

        await websocket.send(message)

# WebSocket 连接
async def connect_websocket():
    try:
        uri = f'ws://{host}:{port}{websocket_path}'
        async with websockets.connect(uri) as websocket:
            print(f'Connected to WebSocket server at {uri}')

            # 启动接收消息和发送消息的任务
            tasks = [
                asyncio.create_task(handle_message(websocket.recv())),
                asyncio.create_task(send_message(websocket))
            ]
            await asyncio.gather(*tasks)

    except websockets.exceptions.ConnectionClosedOK:
        print('WebSocket connection closed')

    except Exception as e:
        print(f'Error: {e}')

# 运行 WebSocket 客户端
async def run_client():
    await connect_websocket()

# 运行客户端
if __name__ == '__main__':
    asyncio.run(run_client())
