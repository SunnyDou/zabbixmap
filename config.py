# -*- coding: utf-8 -*

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    url = "http://IP/zabbix/api_jsonrpc.php"                   #The IP address is the server of zabbix.
    header = {"Content-Type": "application/json"}
    hash_password = 'xxxxxxxxxxxx'
    groupid = ['11']                                            #groupid
    listofhost = [
        'BEIJING'                                           #the hosts list which you want to show.
    ]
    site_info = [
        #[116.445943, 39.972524, "Descriptive text"]
        [116.445943, 39.972524, "地址：北京<br>当前网络流量为："]
    ]

    @staticmethod
    def init_app(app):
        pass

config = {

    'default': Config
}
