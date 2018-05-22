# -*- coding:utf-8 -*-
import datetime,time
import configparser
import requests


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
        conf.read("bms.cfg")
        self.bmsCfg = conf.sections()  # 得到所有的section，并以列表的形式返回
        if self.bmsCfg is None:
            return False
            # 获得指定section中的key的value
        self.url = conf.get("bms_cfg_msg", "URL_ROOT")
        self.user = conf.get("bms_cfg_msg", "USER")
        self.password = conf.get("bms_cfg_msg", "PASSWORD")
        self.system = conf.get("bms_cfg_msg", "SYSTEM")
        self.version = conf.get("bms_cfg_msg", "VERSION")

        return True

    def end(self):
        """ 结束运行 """
        return True

    def login(self):
        url = self.url
        data = self.user + self.password + self.system + self.version
        # 发送请求, 接受响应
        res = requests.post(url=self.url, data=data)
        # 提取token数据
        self.tokenInfo = res.json()['token']
        self.token_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        while True:
            with open("temp/token.txt", "w")as f:
                f.write(self.tokenInfo)

    def run(self):
        self.login()

    # TODO ：1. 调用登录接口，取得token 信息

    # TODO ：2. Token信息保存到 temp/token.txt 文件中

    def waitNextTime(self):
        time.sleep(590)


# TODO ：根据获取Token的有效期，等待相应的时间（考虑到下次操作的时间间隔，需提前10s运行）


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
