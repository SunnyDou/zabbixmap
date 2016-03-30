#!/usr/bin/python2.7
import os
import shutil
from app.models import basedir, showvalues
from config import Config


datadir = "/tmp/data.json"


showvalues(datadir)
os.remove(basedir)
shutil.move(datadir, basedir)
