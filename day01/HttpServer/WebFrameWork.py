#coding = utf-8

'''
功能:完成后端请求处理服务代码
说明:模拟web框架基本原理处理请求,将结果给httpserver
'''

#静态网页存放路径
STATIC_DIR = './static/'
#应用程序存放路径
PYTHON_DIR = './wsgiPy'

#类中完成处理各种请求的具体方法
class Application(object):
    def __init__(self,urls):
        self.urls = urls
    def __call__(self,env,set_headers):
        mothod = env.get('METHOD','GET')
        path = env.get('PATH_INFO','/')
        if not path:
            path = 'index.html'

        if path[-5:] == '.html':
            filename = STATIC_DIR + path
            try:
                fd = open(filename,'rb')
            except IOError:
                status = '404 not found'
                headers = []
                set_headers(status,headers)
                return '<h1>===Sorry not found the page</h1>'
            else:
                status = '200 OK'
                headers = []
                set_headers(status,headers)
                data = fd.read()
                fd.close()
                return data.decode('utf-8')

        #请求python方法
        else:
            for url,handle in self.urls:
                if path == url:
                    status = '200 Ok'
                    headers = []
                    set_headers(status,headers)
                    return handle()
            status = '404 not found'
            headers = []
            set_headers(status,headers)
            return '<h1>Sorry url not found</h1>'

        


#url 处理列表,体现我们能够处理url请求
from wsgiPy import views


urls = [
    ('time',views.show_time),
    ('hello',views.say_hello),
    ('bye',views.say_bye)
    ]



#通过对象完成各种功能调用
app = Application(urls)

