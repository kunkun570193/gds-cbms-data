# -*- coding:utf-8 -*-
import datetime, time
import configparser
import requests
import json
from os.path import exists

glb_LocationMap = {}  # 位置映射表  guid => obj
glb_DeviceMap = {}  # 设备映射表  guid => obj
glb_TagMap = {}  # 指标映射表  guid => obj

# 采集间隔
COLLECT_INTERVAL = 24 * 3600


class bmsCfg():
    """Bms配置采集类"""

    def __init__(self):
        """ 构造函数 """

        self.bmsCfg = None  # bms 配置
        self.tokenInfo = None  # token 信息

    def prepare(self):
        """ 准备运行 """
        conf = configparser.ConfigParser()

        try:
            conf.read("../../config/bms.cfg")
            secs = conf.sections()
            self.system = conf.get("default", "SYSTEM")
            self.version = conf.get("default", "VERSION")
            self.url_root = conf.get("default", "URL_ROOT")
        except Exception as e:
            print(e)

        #   如果和当前时间间隔不足 COLLECT_INTERVAL 则返回False，不做采集
        if exists("../../temp/cfg.tag"):
            with open("../../temp/cfg.tag", "r") as f:
                oldtime = int(f.read())
                nowtime = int(time.time())
                if nowtime - oldtime < COLLECT_INTERVAL:
                    return False

        else:
            nowtime = int(time.time())
            with open("../../temp/cfg.tag", "w")as f:
                f.write(str(nowtime))

        print("采集bms配置成功")
        return True

    def end(self):
        """ 结束运行 """
        nowtime = int(time.time())
        with open("../../temp/cfg.tag", "w")as f:
            f.write(str(nowtime))
        return True

    def run(self):
        header = {}
        with open("../../temp/token.txt", "r")as f:
            self.tokenInfo = f.read()

            if self.tokenInfo is not None:

                header["token"] = self.tokenInfo
            else:
                return False
        print(header)
        url = self.url_root + "/north/config/get"
        param = {"config_version": "12"}

        postparam = {"version": self.version,
                     "system": self.system,
                     "data": param}
        print(postparam)

        res = requests.post(url=url, data=json.dumps(postparam), headers=header)

        if res is None:
            print("res Fail")
            return False

        else:
            config_version = res.json()['data']['config_version']
            if config_version is None:
                print('config_version Fail')
                return False

            else:
                nodes = res.json()['data']['nodes']
                if nodes is None:
                    print("nodes Fail")
                    return False
                else:
                    for node in nodes:
                        if node['node_type'] == 1:
                            glb_LocationMap[node['guid']] = node
                            with open("glb_LocationMap.txt", "a")as f:
                                f.write(str(glb_LocationMap[node['guid']]))

                        elif node['node_type'] == 2:
                            glb_DeviceMap[node['guid']] = node
                            with open("glb_DeviceMap.txt", "a")as f:
                                f.write(str(glb_DeviceMap[node['guid']]))

                        elif node['node_type'] == 3:
                            glb_TagMap[node['guid']] = node
                            with open("glb_TagMap.txt", "a")as f:
                                f.write(str(glb_TagMap[node['guid']]))
                        else:
                            print("Error node type", node['node_type'])
        return True


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
