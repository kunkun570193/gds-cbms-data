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
            conf.read("/home/python/Desktop/BMSAgent/BMSAgent/config/bms.cfg.ini")
            secs = conf.sections()
            print(secs)
        except Exception as e:
            print(False)
            # 获得指定section中的key的value
        self.url_root = conf.get("bms_cfg_msg", "URL_ROOT")
        print(self.url_root)
        self.user = conf.get("bms_cfg_msg", "USER")
        print(self.user)
        self.password = conf.get("bms_cfg_msg", "PASSWORD")
        print(self.password)
        self.system = conf.get("bms_cfg_msg", "SYSTEM")
        print(self.system)

        self.version = conf.get("bms_cfg_msg", "VERSION")
        print(self.version)

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
        print(self.tokenInfo)
        #  获取最大保活时限

        self.timeout = res.json()['data']['timeout']
        print(self.timeout)

        if self.tokenInfo is None:
            print("tonken Fail")

        with open("/home/python/Desktop/gitsource1/gds-cbms-data/agent/temp/token.txt", "w")as f:
            f.write(self.tokenInfo)
            print("ok")

    def run(self):
        self.login()

    # TODO ：1. 调用登录接口，取得token 信息

    # TODO ：2. Token信息保存到 temp/token.txt 文件中

    def waitNextTime(self):

        # TODO ：根据获取Token的有效期，等待相应的时间（考虑到下次操作的时间间隔，需提前10s运行）
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
