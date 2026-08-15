import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os

PORT = 8000
API_URL = "https://aistudio.baidu.com/llm/lmapi/v3/chat/completions"
# 密钥从环境变量读取，避免硬编码泄露（设置方式见 README）
API_KEY = os.environ.get("BAIDU_API_KEY", "")

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                # Forward request to Baidu
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {API_KEY}'
                }
                
                req = urllib.request.Request(API_URL, data=post_data, headers=headers, method='POST')
                
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*') # Allow CORS for local dev
                    self.end_headers()
                    self.wfile.write(response_data)
                    
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.end_headers()
                self.wfile.write(e.read())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if not API_KEY:
    print("WARNING: BAIDU_API_KEY is not set. Set it via environment variable before calling /api/chat.")
print(f"Starting server at http://localhost:{PORT}")
print(f"Open http://localhost:{PORT}/dashboard_system.html to view dashboard")

with socketserver.TCPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
