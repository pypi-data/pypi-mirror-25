from wh import WHMgr

w = WHMgr(u'0-a', 'this is a test message', u'tcp:127.0.0.1:9155')
w.send()
w.run()
print w.confirmed
