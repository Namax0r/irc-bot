#!/usr/local/bin/python

import sys
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor
# ElementTree library to parse XML files
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
# import configuration file.
import config as cfg

tree = ET.ElementTree(file='commandlist.xml')
tree.getroot()


class MyBot(irc.IRCClient):

    nickname = cfg.config['nickname']
    realname = cfg.config['realname']
    username = cfg.config['username']
    password = cfg.config['password']
    channel = cfg.config['channel']

    def signedOn(self):
        self.join(self.channel)
        print 'Signed on as %s' % self.nickname
        self.msg('NickServ', "IDENTIFY %s" % self.password)

    def joined(self, channel):
        print "Joined %s." % channel

    def privmsg(self, user, channel, msg):
        msg=msg.lower() #convert message to lower case
        if '!echo' in msg:
            self.msg(self.channel, msg.replace('!echo', ''))
        for command in tree.findall('command[@name="%s"]' % msg):
            print msg
            rank = command.find('response').text.lstrip()
            self.msg(self.channel, rank)


class MyBotFactory(protocol.ClientFactory):
    protocol = MyBot

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % reason
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % reason

if __name__ == "__main__":
    reactor.connectTCP(cfg.config['serv_addr'], cfg.config['serv_port'], MyBotFactory())
    reactor.run()
