# -*- coding:utf-8 -*-
import datetime, time
import configparser
import requests
import hashlib
import json


class BmsAuth():
    """Bms认证处理类"""

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
            self.url_root = conf.get("default", "URL_ROOT")
            self.user = conf.get("default", "USER")
            self.password = conf.get("default", "PASSWORD")
            self.system = conf.get("default", "SYSTEM")
            self.version = conf.get("default", "VERSION")

        except Exception as e:
            print(e)


        return True

    def end(self):
        """ 结束运行 """
        return True

    def login(self):
        url = self.url_root + "/north/login"
        print(url)
        password = hashlib.md5(str(self.password).encode("utf-8")).hexdigest()
        print(password)

        param = {"password": password, "username": self.user}

        print(param)
        postparam = {"version": self.version,
                     "system": self.system,
                     "data": param}

        postParamStr = json.JSONEncoder().encode(postparam)

        res = requests.post(url=url, data=postParamStr)

        # 提取token数据
        self.tokenInfo = res.json()['data']['token']

        #  获取最大保活时限

        self.timeout = res.json()['data']['timeout']

        if self.tokenInfo is None:
            print("tonken Fail")
        else:
            with open("../../temp/token.txt", "w")as f:
                f.write(self.tokenInfo)
                print("tokenInfo ok")

    def run(self):
        self.login()

    def waitNextTime(self):
        timeout = self.timeout - 10
        time.sleep(timeout)


def main():
    bmsAuth = BmsAuth()

    while True:

        # 初始化
        if bmsAuth.prepare():
            # 运行
            bmsAuth.run()

            # 结束运行
            bmsAuth.end()

            # 等待下次运行
            bmsAuth.waitNextTime()
        else:
            time.sleep(3)


if __name__ == '__main__':
    main()
