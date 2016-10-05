#coding:utf-8
import asyncore, socket,time


class HttpClient(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, 80) )
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path
        self.host = host

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    # автоматически вызывается когда в сокет приходят данные
    # тут мы выведем хост с откуда они идут, и сделаем стандартное чтение с сокета
    def handle_read(self):
        print self.host
        self.recv(8192)
        # print self.recv(8192)

    # этот метод сигнал о том что сокет готов записывать
    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

c = HttpClient('www.mail.ru', '/')
c = HttpClient('www.python.org', '/')

#запускаем цикл опроса сокетов

asyncore.loop(timeout=1)
while True:
    print "pass idle loop"
    time.sleep(0.5)
