from osv.modules import api

api.require('java')

default = api.run_java(args=['-jar jython.jar /app/app.py'])
