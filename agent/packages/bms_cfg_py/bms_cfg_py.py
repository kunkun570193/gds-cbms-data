# -*- coding:utf-8 -*-
import datetime, time
import configparser
import requests
import json


# 采集间隔
COLLECT_INTERVAL = 24 * 3600
glb_LocationMap = {}  # 位置映射表  guid => obj
glb_DeviceMap = {}  # 设备映射表  guid => obj
glb_TagMap = {}  # 指标映射表  guid => obj


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
        with open("../../temp/cfg.tag","r") as f:
            oldtime=int(f.readlines())
            nowtime=int(time.time())
            if nowtime - oldtime < COLLECT_INTERVAL:
                return False

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

        return True

    def end(self):
        """ 结束运行 """
        # TODO : 1. 将当前时间写入 temp/cfg.tag 文件中用以记录采集完成时间
        nowtime = int(time.time())
        with open("../../temp/cfg.tag", "w")as f:
            f.write(str(nowtime))
        return True

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
        # TODO ：3. 将配置采集结果逐条拆分

        config_version = res.json()['data']['config_version']
        if config_version is None:
            print('config_version Fail')

        nodes = res.json()['data']['nodes']
        if nodes is None:
            print("nodes Fail")

        for node in nodes:
            if node['node_type'] == 1:
                glb_LocationMap[node['guid']] = node
                with open("glb_LocationMap.txt","a")as f:
                    f.write(str(glb_LocationMap[node['guid']]))


            elif node['node_type'] == 2:
                glb_DeviceMap[node['guid']] = node
                with open("glb_DeviceMap.txt", "a")as f:
                    f.write(str(glb_DeviceMap[node['guid']]))

            elif node['node_type'] == 3:
                glb_TagMap[node['guid']] = node
                with open("glb_TagMap.txt", "a")as f:
                    f.write(str( glb_TagMap[node['guid']]))
            else:
                print("Error node type", node['node_type'])


def main():
    bmscfg = bmsCfg()

    while True:
        # 初始化
        if bmscfg.prepare():
            # 运行
            bmscfg.run()

            # 结束运行
            bmscfg.end()

        else:
            time.sleep(3)


if __name__ == '__main__':
    main()
