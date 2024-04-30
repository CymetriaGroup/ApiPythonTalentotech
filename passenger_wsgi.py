import sys, os

PROJECT_HOME = "/home/campusbogota/apipy_talento_tech"

sys.path.append(PROJECT_HOME)
sys.path.append(PROJECT_HOME + '/src')

INTERP = "/home/campusbogota/apipy_talento_tech/.virtualenv/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from main import app as application
