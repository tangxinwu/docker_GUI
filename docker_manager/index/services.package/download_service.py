import socketserver


def gen():
    """
    生成器，返回输入的值
    :return:
    """
    __temp_list = list()
    while True:
        data = yield
        if data is None:
            continue
        if data == "stop":
            break
        __temp_list.append(data)
    return __temp_list


def process():
    """
    子调度器
    :return:
    """
    while True:
        yield from gen()


def main():
    """
    调用主函数
    :return:
    """
    g = process()
    next(g)
    while True:
        name = input("请输入值：")
        g.send(name)


class DownloadServer(socketserver.BaseRequestHandler):
    def setup(self):
        print("服务开始。。。")

    def handle(self):
        print("我是self.request", self.request)
        print("我是self.client_address", self.client_address)
        print("我是self.server", self.server)
        print("1")
        while True:
            recived_data = self.request.recv(1).decode("utf8")
            if not recived_data:
                break
            print("我是接受到的数据", recived_data)

    def finish(self):
        print("服务结束。。。")


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 10086), DownloadServer)
    server.serve_forever()
