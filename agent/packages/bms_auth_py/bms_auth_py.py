# -*- coding:utf-8 -*-
import time

class BmsAuth():
    """Bms认证处理类"""
    def __init__(self):
        """ 构造函数 """

        self.bmsCfg = None      # bms 配置
        self.tokenInfo = None   # token 信息

    def prepare(self):
        """ 准备运行 """

        # TODO ：1. 从 config/bms.cfg 文件中读取BMS配置， 失败返回 False

        return True

    def end(self):
        """ 结束运行 """
        return True

    def run(self):
        # TODO ：1. 调用登录接口，取得token 信息

        # TODO ：2. Token信息保存到 temp/token.txt 文件中

    def waitNextTime(self):
        # TODO ：根据获取Token的有效期，等待相应的时间（考虑到下次操作的时间间隔，需提前10s运行）

def main():
    bmsAuth = BmsAuth()
    while True :

        # 初始化
        if bmsAuth.onStart():
            # 运行
            bmsAuth.run()

            # 结束运行
            bmsAuth.end()

            # 等待下次运行
            bmsAuth.sleepToNextTime()
        else :
            time.sleep(3)

if __name__ == '__main__':
    main()
