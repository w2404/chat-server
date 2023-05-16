
import os
import json
import asyncio
import websockets
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 服务器主机和端口
host = 'localhost'
port = 8000

# 静态文件目录
static_dir = '/path/to/static_directory'

# 示例动态数据
dynamic_data = {
    'message': 'Hello, WebSocket!',
    'value': 42
}

# 处理 WebSocket 连接
async def handle_websocket(websocket, path):
    try:
        # 发送初始动态数据
        await websocket.send(json.dumps(dynamic_data))

        # 接收和处理来自客户端的消息
        async for message in websocket:
            # 在这里处理客户端发送的消息，如果需要
            pass

    except websockets.exceptions.ConnectionClosedOK:
        # 连接已关闭
        pass

# 自定义请求处理程序
class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=static_dir, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api'):
            # 将请求转发到 WebSocket 处理函数
            self.handle_websocket()

        else:
            # 使用内置的 SimpleHTTPRequestHandler 处理静态文件
            super().do_GET()

    def handle_websocket(self):
        # 获取 WebSocket 协议
        websocket = self.websocket = websockets.WebSocketServerProtocol(
            self.rfile, self.wfile, 
            origins=None, 
            extensions=None, 
            subprotocols=None,
            extra_headers=None
        )

        # 将请求升级为 WebSocket 连接
        websocket.connection_made(self.connection)

        # 处理 WebSocket 连接
        loop = asyncio.get_event_loop()
        loop.run_until_complete(handle_websocket(self.websocket, self.path))

    def finish(self):
        # 关闭 WebSocket 连接
        if hasattr(self, 'websocket'):
            self.websocket.connection_lost(None)

        super().finish()

# 启动服务器
def run_server():
    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on {host}:{port}')
    httpd.serve_forever()

# 运行服务器
if __name__ == '__main__':
    run_server()
