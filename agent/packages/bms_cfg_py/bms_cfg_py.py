# -*- coding:utf-8 -*-
import datetime,time
import configparser
import requests

# 采集间隔
COLLECT_INTERVAL = 24*3600

class bmsCfg():
    """Bms配置采集类"""

    def __init__(self):
        """ 构造函数 """

        self.bmsCfg = None  # bms 配置
        self.tokenInfo = None  # token 信息

    def prepare(self):
        """ 准备运行 """

        # TODO : 1. 从 temp/cfg.tag 文件中读取上次采集时间，
        #   如果和当前时间间隔不足 COLLECT_INTERVAL 则返回False，不做采集

        # TODO ：1. 从 config/bms.cfg 文件中读取BMS配置， 失败返回 False

        return True

    def end(self):
        """ 结束运行 """
        # TODO : 1. 将当前时间写入 temp/cfg.tag 文件中用以记录采集完成时间

        return True

    def run(self):

        # TODO : 1. 从 temp/token.txt 文件中读取token信息

        # TODO ：2. 发送配置采集请求

        # TODO ：3. 将配置采集结果逐条拆分

def main():
    bmsCfg = bmsCfg()

    while True:
        # 初始化
        if bmsCfg.prepare():
            # 运行
            bmsCfg.run()

            # 结束运行
            bmsCfg.end()

        else:
            time.sleep(3)

if __name__ == '__main__':
    main()
