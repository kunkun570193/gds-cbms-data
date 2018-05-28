# -*- coding:utf-8 -*-
import datetime, time
import configparser
import requests
import json


class BmsAlarm():
    def __init__(self):
        """ 构造函数 """

        self.bmsCfg = None  # bms 配置
        self.tokenInfo = None  # token 信息

    def prepare(self):
        """ 准备运行 """
        # TODO ：1. 从 config/bms.cfg 文件中读取BMS配置， 失败返回 False
        conf = configparser.ConfigParser()

        try:
            conf.read("../../config/bms.cfg")
            secs = conf.sections()
            print(secs)
        except Exception as e:
            print(False)
            # 获得指定section中的key的value
        self.system = conf.get("default", "SYSTEM")
        self.version = conf.get("default", "VERSION")
        self.url_root = conf.get("default", "URL_ROOT")

    def end(self):
        """ 结束运行 """
        return  True

    def run(self):

        # TODO : 1. 从 temp/token.txt 文件中读取token信息
        with open("../../temp/token.txt", "r")as f:
            token =f.read()
            print(token,"token")
            header = {}
            if token is not None:

                header["token"] = token
                print(header,"header")

        # TODO ：2. 发送配置采集请求
        url = self.url_root + "/north/config/get"
        param = {"config_version": "12"}


        postparam = {"version": self.version,
                     "system": self.system,
                     "data": param}

        res = requests.post(url=url, data=json.dumps(postparam), headers=header)
        if res is None:
            print("res Fail")
        # TODO ：3. 将报警解析





def main():
    bmsalarm=BmsAlarm()
    while True:
        if bmsalarm.prepare():

            bmsalarm.run()

            bmsalarm.end()
        else:
            time.sleep(3)

if __name__ == '__main__':
    main()

