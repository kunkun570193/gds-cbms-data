# -*- coding:utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import queue
import json,time
import gzip
import rt_helper


H = rt_helper.RtHelper()
H.setLogger('bms_rt')

# 全局对象

# 消息队列数量
glb_ThreadNum = 10

# 消息队列
glb_Queue = None
# 配置消息处理对象
class CfgMsgProcessor():
    # 处理消息
    def processMsg(self, msgBody):

        # 连接 mananger 的 redis
        r = H.connectManagerRedis()

        result = json.loads(msgBody.decode("utf-8"))
        res = result['nodes']
        nodes = json.dumps(res)

        config_version=msgBody['config_version']
        H.writeTempFile("config_version.txt", config_version)

        cnt = 1
        while len(nodes) > 0:
            #  最多1000条记录一个包
            popLen = min(1000, len(nodes))

            data_list = nodes[:popLen]
            nodes = nodes[popLen:]

            # 打包json数据
            jsonStr = json.dumps({
                'dc_id': 46,
                'data': data_list
            })
            jsonBin = gzip.compress(jsonStr.encode('utf8'))
            r.lpush("cfg", jsonBin)

            H.logger.info("发送配置数据 %s ~ %s , 长度 %s", cnt, cnt + popLen, len(jsonBin))
            cnt += popLen
            time.sleep(5)
        return True

#
# 性能消息处理对象
#
class PmMsgProcessor():
    #
    # 处理消息
    #
    def processMsg(self, msgBody):
        pass
#
# 告警消息处理对象
#
class AlarmMsgProcessor():
    #
    # 处理消息
    #
    def processMsg(self, msgBody):
        # 连接 mananger 的 redis
        r = H.connectManagerRedis()

        H.logger.info("链接redis成功")

        result = json.loads(msgBody.decode("utf-8"))
        data_list = [result['data']]

        if len(data_list) > 0:
            # 打包json数据
            jsonStr = json.dumps({
                'dc_id': 46,
                'data': data_list
            })

            jsonBin = gzip.compress(jsonStr.encode('utf8'))

            r.lpush("alarm", jsonBin)

            H.logger.info("发送离线告警数据长度 %s",  len(jsonBin))
            time.sleep(5)

        return True


#
# 消息队列对象
#
class MsgQueue():

    def __init__(self):
        # self.queue = None  # 创建消息对象
        self.queue = queue.Queue()

    # 将参数中的消息推送到消息队列
    def pushMsg(self, msgType, msgBody):

        self.queue.put((msgType,msgBody))

    # 从消息队列中取1条消息，返回 msgType, msgBody
    def popMsg(self):
        while True:
            try:
                msg=self.queue.get()

            except queue.Empty:
               continue
            else:
                return msg
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
            msgType,msgBody = glb_Queue.popMsg()


           # # 循环消息处理列表
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
        self.send_error(code)
        # step 2 : 如果data内容不为空，则返回data内容
        if not data:
            return data

    def do_GET(self):
        self.sendBackError(4, "pattern error")

    def do_POST(self):
        # step 1 : 解析请求的URL , 数据对象
        # urlStr = "解析出的URL"
        urlStr = self.path

        # postObj = "解析出的数据参数"
        postObj = self.rfile.read(int(self.headers['content-length']))
        if postObj is None:

            return self.sendBackError(4, "postObj is None")

        else:
            # step 2.1 : 根据不通消息类型，处理数据对象
            global glb_Queue
            # step 2.1.1 如果是推送消息的url请求
            if urlStr == "/north/config/push":
                #   此处不做处理将消息直接发送到消息队列

                glb_Queue.pushMsg("cm", postObj)


            # step 2.1.2 如果是推送性能的url请求
            elif urlStr == "/north/data/online/push":
                #   此处不做处理将消息直接发送到消息队列

                glb_Queue.pushMsg("pm", postObj)

            # step 2.1.3 如果是推送告警的url请求
            elif urlStr == "/north/alarm/online/push":
                #   此处不做处理将消息直接发送到消息队列
                glb_Queue.pushMsg("am", postObj)

            # step 2.1.4 否则返回错误信息
            #   不是主动推送请求，返回错误信息
            else:
                self.sendBackError(4, "NOT PUSH")

        # step 2.2 返回调用成功与否的信息
        self.sendBackSuccess("result:success")
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", 0)
        self.end_headers()

def main():
    global glb_Queue

    # 初始化全局对象
    glb_Queue = MsgQueue()

    threadAry = []
    for i in range(0, glb_ThreadNum):
        thread = WorkThread()
        threadAry.append(thread)
        thread.start()

    server_address = ('', 35080)
    httpd = HTTPServer(server_address, PushHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
