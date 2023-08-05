from txtorcon import (TorConfig, launch_tor, build_tor_connection,
                      DEFAULT_VALUE, TorClientEndpoint)
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import clientFromString
from time import sleep

class Gama(object):

    def __init__(self):
        self.react = reactor
        print 1

    @inlineCallbacks
    def main(self):
        try:
            ep = clientFromString(self.react, u'tcp:127.0.0.1:9155')
            self.tor = yield build_tor_connection(ep, build_state=False)
            self.tconfig = yield TorConfig.from_protocol(self.tor)
            sleep(5)
            print 2
            self.react.stop()
            sleep(5)
            print 8
        except Exception:
            raise
        return

if __name__ == '__main__':
    print 3
    tor = Gama()
    print 4
    tor.main()
    print 5
    tor.react.run()
    print 6
    sleep(5)
    print 7


