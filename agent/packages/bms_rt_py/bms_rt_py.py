# import BaseHTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import threading
import queue

#
# 全局对象
#

# 消息队列数量
glb_ThreadNum = 10

# 消息队列
glb_Queue = None


#
#
# 配置消息处理对象
#
class CfgMsgProcessor():
    #
    # 处理消息
    #
    def processMsg(msg):
        pass


#
# 性能消息处理对象
#
class PmMsgProcessor():
    #
    # 处理消息
    #
    def processMsg(msg):
        pass


#
# 告警消息处理对象
#
class AlarmMsgProcessor():
    #
    # 处理消息
    #
    def processMsg(msg):
        pass


#
# 消息队列对象
#
class MsgQueue():
    def __init__(self):
        # self.queue = None  # 创建消息对象
        self.q = queue.Queue()

    # 将参数中的消息推送到消息队列
    def pushMsg(self, msgType, msgBody):
        msgType = self.q.put(msgType)
        msgBody = self.q.put(msgBody)

    # 从消息队列中取1条消息，返回 msgType, msgBody
    def popMsg(self):
        msgType, msgBody = self.q.get()


#
# 线程对象
#
class WorkThread(threading.Thread):
    def run(self):
        # step 1 : 初始化消息处理对象
        cfgMsgProcessor = CfgMsgProcessor()
        pmMsgProcessor = PmMsgProcessor()
        alarmMsgProcessor = AlarmMsgProcessor()

        # step2 : 从消息队列中取数据并处理
        global glb_Queue
        while True:
            msgType, msgBody = glb_Queue.popMsg()

            # 循环消息处理列表
            if msgType == 'cm':
                cfgMsgProcessor.processMsg(msgBody)
            elif msgType == 'pm':
                pmMsgProcessor.processMsg(msgBody)
            elif msgType == 'am':
                alarmMsgProcessor.processMsg(msgBody)


#
# http server 处理类
#
class PushHandler(BaseHTTPRequestHandler):
    def sendBackSuccess(self, data):
        # step 1 : 返回成功消息200
        self.send_response(200)
        # step 2 : 如果data内容不为空，则返回data内容
        if not data:
            return data

    def sendBackError(self, code, data):
        # step 1 : 返回错误号 code
        self.send_error(500)
        # step 2 : 如果data内容不为空，则返回data内容
        if not data:
            return data

    def do_GET(self):
        self.sendBackError(500, "result:fail")

    def do_POST(self):
        # step 1 : 解析请求的URL , 数据对象
        # urlStr = "解析出的URL"
        parsed_result = urlparse(self.path)
        urlStr = parsed_result.path
        # postObj = "解析出的数据参数"
        length = self.headers.getheader('content-length')
        nbytes = int(length)
        postObj = self.rfile.read(nbytes)

        # datas = self.rfile.read(int(self.headers['content-length']))

        # step 2.1 : 根据不通消息类型，处理数据对象

        # step 2.1.1 如果是推送消息的url请求
        if urlStr == "/north/config/push":
            #   此处不做处理将消息直接发送到消息队列
            postObj.pushMsg()
        # step 2.1.2 如果是推送性能的url请求
        elif urlStr == "/north/data/online/push":
            #   此处不做处理将消息直接发送到消息队列
            postObj.pushMsg()
        # step 2.1.3 如果是推送告警的url请求
        elif urlStr == "/north/alarm/online/push":
            #   此处不做处理将消息直接发送到消息队列
            postObj.pushMsg()
        # step 2.1.4 否则返回错误信息
        #   不是主动推送请求，返回错误信息
        else:
            self.send_error("NOT PUSH")

        # step 2.2 返回调用成功与否的信息
        self.sendBackSuccess("result:success")


def main():
    global glb_Queue

    # 初始化全局对象
    glb_Queue = MsgQueue()

    # TODO : 根据消息队列数量启动线程
    threadAry = []
    for i in range(0, glb_ThreadNum):
        thread = WorkThread()
        # threadAry.push(thread)
        threadAry.append(thread)
        thread.start()

    server_address = ('', 35080)
    httpd = HTTPServer(server_address, PushHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
