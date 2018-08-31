#coding = utf-8

'''
name:yangli
功能：完成httpserver项目
        httpserver部分
'''

from socket import *
import sys
from threading import Thread
import re

#将httpserver具体内容封装为类
class HTTPServer(object):
    def __init__(self,app):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.app = app

    def bind(self,ip='0.0.0.0',port='8080'):
        self.ip = ip 
        self.port = port
        self.sockfd.bind((ip,port))

    def serve_forever(self):
        self.sockfd.listen(10)
        print('Listen to the port %d' % self.port)
        while True:
            c,addr = self.sockfd.accept()
            print('connect from :',addr)
            handle_thread = Thread(target = self.handle_client,args= (c,))
            handle_thread.setDaemon(True)
            handle_thread.start()
    #处理具体的客户端请求
    def handle_client(self,c):
        #接收浏览器的request
        request_data = c.recv(1024)
        request_lines = request_data.splitlines()
        #获取请求行GET/ HTTP1.1
        request_line = request_lines[0].decode('utf-8')
        #使用正则表达式匹配出请求方法和请求内容
        env = re.match\
        (r'(?P<METHOD>\w+)\s+/(?P<PATH_INFO>\S*)',\
            request_line).groupdict()
        #生产的方法和请求的内容为如下字典
        # env = {'METHOD': 'GET', 'PATH_INFO': 'tedu.html'}
        #将env交给WebFrameWork中app处理
        response_body = self.app(env,self.set_headers)
        #将响应结果给客户端
        response = self.response_headers + '\r\n' + response_body
        #回发给客户
        c.send(response.encode())
        c.close()

    #拼接响应头,响应行
    def set_headers(self,status,headers):
        '''
        两个参数希望得到的值
        status = '200 ok'
        hearders = [
        ("Content-Type","text/plain"),
        ()
        ]
        '''
        response_headers = 'HTTP/1.1' + status + '\r\n'
        for header in headers:
            response_headers += '%s:%s\r\n' % header
        self.response_headers = response_headers



#创建httpserver对象,添加必要属性,启动服务程序
def main():
    #启动httpserver时从命令行直接输入使用的应用服务模块
    if len(sys.argv) < 2:
        sys.exit('''
            run the server as 
            python3 HttpServer.py FrameWorkName:app
            ''')
    #提取出模块和app名称
    module_name,app_name = sys.argv[1].split(':')
    #将当前的路径加入到环境变量
    sys.path.insert(1,'.')
    #导入模块,生成模块对象
    m = __import__(module_name)
    #获取APP对象
    app = getattr(m,app_name)

    #使app成为httpd的属性,处理具体请求事件
    httpd = HTTPServer(app)
    httpd.bind('0.0.0.0',8000)
    #启动服务器
    httpd.serve_forever()




if __name__ == '__main__':
    main()