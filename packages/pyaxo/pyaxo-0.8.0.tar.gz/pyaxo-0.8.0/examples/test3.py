from wh import WHMgr

w = WHMgr(u'0-a', None, u'tcp:127.0.0.1:9155')
w.receive()
w.run()
print w.data
