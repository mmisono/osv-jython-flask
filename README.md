# Jython-Flask Sample Application on OSv
This is simple blog powerd by flask on jython on OSv. The blog is based on [flask tutorial](http://flask.pocoo.org/docs/tutorial/introduction/).

## 問題点
- 何故かflaskをimportする前にBytesIOをimportしておかないとjythonでエラーが発生する. (BytesIOが無いと怒られる)
- sqlite-jdbc.jar を動的にロードできなかったのでantでjython.jarにマージしている ([本当はこれがしたい](http://www.jython.org/jythonbook/en/1.0/appendixB.html#working-with-classpath))
