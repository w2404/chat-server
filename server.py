import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 服务器主机和端口
host = '0.0.0.0' #localhost'
port = 8000

# 静态文件目录
static_dir = './static' 

# 示例动态 JSON 数据
dynamic_data = {
    'message': 'Hello, World!',
    'value': 42
}

# 自定义请求处理程序
class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=static_dir, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api'):
            self.serve_dynamic_data()
        else:
            # 使用内置的 SimpleHTTPRequestHandler 处理静态文件
            super().do_GET()

    def serve_dynamic_data(self):
        try:
            # 设置响应头
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # 发送动态 JSON 数据
            response_data = json.dumps(dynamic_data)
            self.wfile.write(response_data.encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

# 启动服务器
def run_server():
    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on {host}:{port}')
    httpd.serve_forever()

# 运行服务器
if __name__ == '__main__':
    run_server()
