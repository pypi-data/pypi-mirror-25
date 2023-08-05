import wormhole
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from wormhole.cli.public_relay import RENDEZVOUS_RELAY

react = reactor
appid = u'123'
relay_url = RENDEZVOUS_RELAY
@inlineCallbacks
def go():
    def pr(message):
        print message
    w = wormhole.create(appid, relay_url, react)
    code = unicode(raw_input('Code: '))
    w.set_code(code)
    w.send_message(b"outbound data")
    inbound = yield w.get_message().addCallback(pr)
    yield w.close()
    react.stop()

if __name__ == '__main__':
    go()
    react.run()
