# -*- coding:utf-8 -*-
import configparser
import redis
import pymysql
import json

class CfgProcess():
    def __init__(self):
        """ 构造函数 """
        self.redisH = None
        self.mainDB = None

    def prepare(self):
        """ 准备运行 """
        # 1. 从 config/redis.cfg 文件中读取redis配置， 失败返回 False
        self.connectRedis()

        return True

    def end(self):
        """ 结束运行 """
        self.redisH = None
        self.mainDB = None
        return  True

    def run(self):
        # 循环读取Q中的消息
        while True:
            # 1. 从Q中收取一条消息, 等待120没有消息，则重连Q
            data = self.redisH.blpop('cfg', 120)
            if not data or len(data) < 2:
                return

            # 2. 取消息
            msgBody = data[1]

            # 3. 入库
            self.process(msgBody)

    # 连接数据库
    def connectMainDB(self):
        if self.mainDB:
            self.mainDB = None

        # 1. 从 config/redis.cfg 文件中读取redis配置， 失败返回 False
        cfg = configparser.ConfigParser()
        cfg.read('../../config/db.cfg')

        # 2. 连接mysql
        self.mainDB = pymysql.connect(
            host = cfg.get('main', 'DB_HOST'),
            port = int(cfg.get('main', 'DB_PORT')),
            db = cfg.get('main', 'DB_NAME'),
            user = cfg.get('main', 'DB_USER'),
            password = cfg.get('main', 'DB_PASSWD'))


    # 连接数据库
    def connectRedis(self):
        if self.redisH :
            self.redisH = None

        # 1. 从 config/redis.cfg 文件中读取redis配置， 失败返回 False
        cfg = configparser.ConfigParser()
        cfg.read('../../config/redis.cfg')

        # 2. 连接redis
        self.redisH = redis.StrictRedis(
            host = cfg.get('default', 'RDS_HOST'),
            port = int(cfg.get('default', 'RDS_PORT')),
            db = int(cfg.get('default', 'RDS_DB')))

        return True

    # 信息入库
    def process(self, msg):
        print(msg)

        # 1. 连接数据库
        if not self.mainDB:
            self.connectMainDB()
            if not self.mainDB:
                return

        # 2. 连接数据库
        msgObj = json.JSONDecoder().decode(msg.decode('utf8'))
        dcId = msgObj['dc_id']
        cfgRows = msgObj['data']

        # 3. 处理配置记录
        for row in cfgRows:
            # 设备和位置都作为位置节点处理
            if row['node_type'] in (1,2):
                print(row)
                pass

            # 处理节点信息
            if row['node_type'] == 3:
                print(row)
                pass

def main():
    cfgProcess = CfgProcess()
    while True:
        if cfgProcess.prepare():

            cfgProcess.run()

            cfgProcess.end()
        else:
            time.sleep(3)

if __name__ == '__main__':
    main()
