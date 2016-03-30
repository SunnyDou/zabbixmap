# -*- coding: utf-8 -*

from flask import render_template
from . import main
from ..models import showvalues, basedir
from config import Config
import os
import json


@main.route('/zabbixmap')
def zabbixmap():
    if os.path.exists(basedir):
        pass
    else:
        showvalues(basedir)
    showvalue = json.dumps(json.load(open(basedir, 'r')))
    return render_template("index.html", site_info=json.dumps(Config.site_info), showvalue=showvalue)
