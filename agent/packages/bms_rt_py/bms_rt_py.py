import BaseHTTPServer

#
# 全局对象
#

# 消息队列数量
glb_ThreadNum = 10

# 消息队列
glb_Queue = None


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
class PmMsgProcessor(MsgProcessorBase):
    #
    # 处理消息
    #
    def processMsg(msg):
        pass

#
# 告警消息处理对象
#
class AlarmMsgProcessor(MsgProcessorBase):
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
        self.queue = None # 创建消息对象

    # 将参数中的消息推送到消息队列
    def pushMsg(self, msgType, msgBody):
        pass

    # 从消息队列中取1条消息，返回 msgType, msgBody
    def popMsg(self):
        pass

#
# 线程对象
#
class WorkThread(threading.Thread):
    def run(self) :
        # step 1 : 初始化消息处理对象
        cfgMsgProcessor = CfgMsgProcessor()
        pmMsgProcessor = PmMsgProcessor()
        alarmMsgProcessor = AlarmMsgProcessor()

        # step2 : 从消息队列中取数据并处理
        global glb_Queue
        while True:
            msgType, msgBody = glb_Queue.popMsg()

            # 循环消息处理列表
            if msgType == 'cm' :
                cfgMsgProcessor.processMsg(msgBody)
            elif msgType == 'pm' :
                pmMsgProcessor.processMsg(msgBody)
            elif msgType == 'am' :
                alarmMsgProcessor.processMsg(msgBody)

#
# http server 处理类
#
class PushHandler(BaseHTTPServer.BaseHTTPRequestHandler): 
    def sendBackSuccess(self, data):
        # step 1 : 返回成功消息200

        # step 2 : 如果data内容不为空，则返回data内容

    def sendBackError(self, code, data):
        # step 1 : 返回错误号 code

        # step 2 : 如果data内容不为空，则返回data内容

    def do_GET(self):
        self.sendBackError(500, "")

    def do_POST(self):
        # step 1 : 解析请求的URL , 数据对象
        urlStr = "解析出的URL"
        postObj = "解析出的数据参数"

        # step 2.1 : 根据不通消息类型，处理数据对象

        # step 2.1.1 如果是推送消息的url请求
        #   此处不做处理将消息直接发送到消息队列

        # step 2.1.2 如果是推送性能的url请求
        #   此处不做处理将消息直接发送到消息队列

        # step 2.1.3 如果是推送告警的url请求
        #   此处不做处理将消息直接发送到消息队列

        # step 2.1.4 否则返回错误信息
        #   不是主动推送请求，返回错误信息

        # step 2.2 返回调用成功与否的信息

def main():
    global glb_Queue

    # 初始化全局对象
    glb_Queue = MsgQueue()

    # TODO : 根据消息队列数量启动线程 
    threadAry = []
    for i in range(0, glb_ThreadNum):
        thread = WorkThread()
        threadAry.push(thread)
        thread.start()

    server_address = ('', 35080)
    httpd = server_class(BaseHTTPServer.HTTPServer, PushHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    main()


