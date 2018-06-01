# -*- coding:utf-8 -*-
import datetime, time
import configparser
import requests
import json
from os.path import exists
import redis

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

        # 如果和当前时间间隔不足 COLLECT_INTERVAL 则返回False，不做采集
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

        if exists("../../config/config_version.txt"):
            with open("../../config/config_version.txt", "r") as f:
                self.config_version = f.read()
        else:
            self.config_version = 12

        url = self.url_root + "/north/config/get"
        param = {"config_version": self.config_version}

        postparam = {"version": self.version,
                     "system": self.system,
                     "data": param}

        res = requests.post(url=url, data=json.dumps(postparam), headers=header)

        if res is None:
            print("res Fail")
            return False

        else:
            config_version = res.json()['data']['config_version']
            nodes = res.json()['data']['nodes']

            if config_version and nodes is not None:
                with open("../../config/config_version.txt", "w")as f:
                    f.write(str(config_version))

        cfg = configparser.ConfigParser()

        cfg.read('../../config/manager.cfg')


        # 2. 连接redis

        pool = redis.ConnectionPool(host=cfg.get('redis', 'RDS_HOST'),
                                port=int(cfg.get('redis', 'RDS_PORT')),
                                db=int(cfg.get('redis', 'RDS_DB')))
        r = redis.Redis(connection_pool=pool)

        data_list = []
        nodes = res.json()['data']['nodes']
        for node in nodes:
            x=data_list.count(node)
            if x < 1000:
                data_list.append(node)
                x += 1

            dc_id = ("'dc_id':46" ,data_list)

            js_data = json.dumps(dc_id,ensure_ascii=False)

            r.lpush("cfg", js_data)


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
