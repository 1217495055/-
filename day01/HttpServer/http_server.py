try:
    #python2方法
    from BaseHTTPServer import \
    BaseHTTPRequestHandler,HTTPServer
except ImportError:
    #python3方法
    from http.server import \
    BaseHTTPRequestHandler,HTTPServer

#处理具体请求
class RequestHandle(BaseHTTPRequestHandler):
    def do_GET(self):
        #请求头
        print(self.headers)
        #请求方法
        print(self.command)
        #具体请求内容
        print(self.path)
        print('Do method get')
        fd = open('test.html','rb')
        content = fd.read()
        #响应行
        self.send_response(200)
        #响应头
        self.send_header('Content-Type','text/html')
        #响应头结束
        self.end_headers()
        #发送响应体
        self.wfile.write(content)
        return
    def do_POST(self):
        pass
    def do_PUT(self):
        pass
    def do_HEAD(self):
        pass
#制定服务器地址
address = ('0.0.0.0',8080)
#创建服务器对象
server = HTTPServer(address,RequestHandle)
#运行服务器
server.serve_forever()
