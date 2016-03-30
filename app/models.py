import json
import urllib2
from config import Config
import os
import re


basedir = os.path.abspath(os.path.dirname(__file__)) + "\\templates\\data.json"


def getgrouplist():
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": ["groupid", "name"],
            },
            "auth": Config.hash_password,
            "id": 1,
        })
    request = urllib2.Request(Config.url, data)
    for key in Config.header:
        request.add_header(key, Config.header[key])
    result = urllib2.urlopen(request)
    response = json.loads(result.read())
    result.close()
    return response['result']


def gethostlist(groupid):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "name"],
                "groupids": groupid,
            },
            "auth": Config.hash_password,
            "id": 1,
        })
    request = urllib2.Request(Config.url, data)
    for key in Config.header:
        request.add_header(key, Config.header[key])
    result = urllib2.urlopen(request)
    response = json.loads(result.read())
    result.close()
    listofhost = {}
    for host in response['result']:
        listofhost[host['name']] = host['hostid']
    return listofhost


def getitemlist(hostid):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": ["itemids", "key_"],
                "hostids": hostid,
            },
            "auth": Config.hash_password,
            "id": 1,
        })
    request = urllib2.Request(Config.url, data)
    for key in Config.header:
        request.add_header(key, Config.header[key])
    result = urllib2.urlopen(request)
    response = json.loads(result.read())
    result.close()
    listofitem = {}
    for item in response['result']:
        listofitem[item['key_']] = item['itemid']
    return listofitem


def getitemvalue(keyid):
    data = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 3,
                "itemids": keyid,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 1,
            },
            "auth": Config.hash_password,
            "id": 1,
        })
    request = urllib2.Request(Config.url, data)
    for key in Config.header:
        request.add_header(key, Config.header[key])
    result = urllib2.urlopen(request)
    response = json.loads(result.read())
    result.close()
    valueofkey = {}
    for key in response['result']:
        valueofkey[key['itemid']] = key['value']
    return valueofkey


def secondtoday(seconds):
    minute = (int(seconds) / 60) % 60
    hour = ((int(seconds) / 60) / 60) % 24
    day = ((int(seconds) / 60) / 60) / 24
    return [minute, hour, day]


def showvalues(datadir):
    listofgroup = {}
    for groupid in Config.groupid:
        hostlist = gethostlist(groupid)
        listofhost = []
        for hostname in Config.listofhost:
            listofitem = []
            listofnetwork = []
            networkflow = 0
            hostid = hostlist[hostname]
            itemlist = getitemlist(hostid)
            for itemkey in itemlist.keys():
                networktrue = re.match(r'ifOutOctets.*WAN.*', itemkey)
                quanzhou = re.match(r'ifOutOctets.*1/0/23.*', itemkey)
                if itemkey == 'sysUpTime':
                    itemid = itemlist[itemkey]
                    itemvalue = getitemvalue(itemid)
                    if itemvalue:
                        listofitem.append(itemvalue[itemid])
                    else:
                        listofitem.append('0')
                elif itemkey == 'icmpping':
                    itemid = itemlist[itemkey]
                    itemvalue = getitemvalue(itemid)
                    if itemvalue:
                        listofitem.append(itemvalue[itemid])
                    else:
                        listofitem.append('0')
                elif networktrue or quanzhou:
                    itemid = itemlist[itemkey]
                    itemvalue = getitemvalue(itemid)
                    if itemvalue:
                        listofnetwork.append(itemvalue[itemid])
                    else:
                        listofnetwork.append('0')
                else:
                    continue
            for i in range(0, len(listofnetwork)):
                networkflow += int(listofnetwork[i])
            listofitem.append(networkflow / 1024 / 1024.00)
            listofhost.append(listofitem)
        listofgroup[groupid] = listofhost
    json.dump(listofgroup, open(datadir, 'w'))
