#!/usr/bin/env python3
#
# This file is part of sarracenia.
# The sarracenia suite is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2008-2015
#
# Questions or bugs report: dps-client@ec.gc.ca
# sarracenia repository: git://git.code.sf.net/p/metpx/git
# Documentation: http://metpx.sourceforge.net/#SarraDocumentation
#
# sr_winnow.py : python3 program allowing to winnow duplicated messages
#                and post the unique and first message in.
#
#
# Code contributed by:
#  Michel Grenier - Shared Services Canada
#  Murray Rennie  - Shared Services Canada
#  Last Changed   : Dec  8 15:22:58 GMT 2015
#  Last Revision  : Jan  8 15:03:11 EST 2016
#  Last Revision  : Apr  11 09:00:00 CDT 2016
#
########################################################################
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, 
#  but WITHOUT ANY WARRANTY; without even the implied warranty of 
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#
#

import os,sys,time

try :    
         from sr_amqp           import *
         from sr_cache          import *
         from sr_consumer       import *
         from sr_instances      import *
         from sr_message        import *
         from sr_util           import *
except : 
         from sarra.sr_amqp      import *
         from sarra.sr_cache     import *
         from sarra.sr_consumer  import *
         from sarra.sr_instances import *
         from sarra.sr_message   import *
         from sarra.sr_util      import *

class sr_winnow(sr_instances):

    def __init__(self,config=None,args=None):
        if config == None:
           self.help()
           return

        sr_instances.__init__(self,config,args)

    def check(self):

        # no queue name allowed

        if self.queue_name == None:
           self.queue_name  = 'q_' + self.broker.username + '.'
           self.queue_name += self.program_name + '.' + self.config_name 

        # we cannot have more than one instance since we 
        # need to work with a single cache.

        if self.nbr_instances != 1 :
           self.logger.warning("Only one instance allowed... set to 1")
           self.nbr_instances = 1

        # exchange must be provided 
        if self.exchange == None:
           self.logger.error("exchange (input) unset... exitting")
           sys.exit(1)

        # post_exchange must be provided
        if self.post_exchange == None :
           self.logger.error("post_exchange (output) not properly set...exitting")
           sys.exit(1)

        # post_exchange must be different from exchange if on same broker
        if not self.post_broker and self.post_exchange == self.exchange :
           self.logger.error("post_exchange (output) not properly set...exitting")
           sys.exit(1)

        if not self.post_broker : self.post_broker = self.broker

        # no vip given... so should not matter ?
        if self.vip == None and self.interface == None :
           self.logger.debug("both vip and interface missing... standalone mode")

        # bindings should be defined 

        if self.bindings == []  :
           key = self.topic_prefix + '.#'
           self.bindings.append( (self.exchange,key) )
           self.logger.debug("*** BINDINGS %s"% self.bindings)

        # accept/reject
        self.use_pattern          = self.masks != []
        self.accept_unmatch       = True

    def close(self):
        self.consumer.close()

        if self.post_broker :
           self.post_hc.close()

        if self.cache  : 
           self.cache.save()
           self.cache.close()

    def connect(self):

        # =============
        # create message
        # =============

        self.msg = sr_message(self)

        # =============
        # consumer
        # =============

        self.consumer             = sr_consumer(self)
        self.msg.report_publisher = self.consumer.publish_back()
        self.msg.report_exchange  = self.report_exchange
        self.msg.user             = self.broker.username

        self.logger.info("reading from to %s@%s, exchange: %s" %
               ( self.broker.username, self.broker.hostname, self.msg.exchange ) )
        self.logger.info("report_back is %s to %s@%s, exchange: %s" %
               ( self.reportback, self.broker.username, self.broker.hostname, self.msg.report_exchange ) )

        self.post_hc = self.consumer.hc

        # =============
        # if post_broker different from broker
        # =============

        if self.post_broker :
           self.post_hc  = HostConnect( self.logger )
           self.post_hc.set_url(self.post_broker)
           self.post_hc.connect()

           self.msg.user = self.post_broker.username

           self.logger.info("Output AMQP broker(%s) user(%s) vhost(%s)" % \
                           (self.post_broker.hostname,self.post_broker.username,self.post_broker.path) )
        else:
           self.logger.info("Output AMQP broker(%s) user(%s) vhost(%s)" % \
                           (self.broker.hostname,self.broker.username,self.broker.path) )

        # =============
        # publisher if post_broker is same as broker
        # =============

        self.publisher = Publisher(self.post_hc)
        self.publisher.build()
        self.msg.publisher = self.publisher

        self.msg.pub_exchange  = self.post_exchange
        self.msg.post_exchange_split  = self.post_exchange_split
        self.logger.info("Output AMQP exchange(%s)" % self.msg.pub_exchange )

        # =============
        # amqp resources
        # =============

        self.declare_exchanges()

        # =============
        # cache
        # =============

        self.cache = sr_cache(self)
        self.cache.open()

    def overwrite_defaults(self):

        # default broker : manager

        self.broker      = None
        self.post_broker = None
        if hasattr(self,'manager'):
           self.broker   = self.manager

        self.cache       = None

        # caching by default (20 mins)

        self.caching     = 1200
        self.cache_stat  = True

        # heartbeat to clean/save cache

        self.execfile("on_heartbeat",'heartbeat_cache')
        self.on_heartbeat_list.append(self.on_heartbeat)
        

    def help(self):
        print("Usage: sr_winnow [OPTIONS] [foreground|start|stop|restart|reload|status|cleanup|setup] configfile\n" )
        print("version: %s \n" % sarra.__version__ )
        print("read file announcements from exchange and reannounce them to post_exchange, suppressing duplicates\n")
        print("OPTIONS:")
        print("-b   <broker>                default manager (if configured)")
        print("-e   <exchange>              MANDATORY")
        print("-tp  <topic_prefix>          default v02.post")
        print("-st  <subtopic>              default #")
        print("-pe  <post_exchange>         MANDATORY")
        print("DEBUG:")
        print("-debug")

    # =============
    # __on_message__
    # =============

    def __on_message__(self):

        # invoke user defined on_message when provided

        for plugin in self.on_message_list:
           if not plugin(self): return False

        return True

    # =============
    # __on_post__ posting of message
    # =============

    def __on_post__(self):

        # invoke on_post when provided

        for plugin in self.on_post_list :
           if not plugin(self): return False

        ok = self.msg.publish( )

        return ok

    # =============
    # process message  
    # =============

    def process_message(self):

        self.logger.debug("Received %s '%s' %s  filesize: %s" % (self.msg.topic,self.msg.notice,self.msg.hdrstr,self.msg.filesize))

        #=================================
        # now message is complete : invoke __on_message__
        #=================================

        ok = self.__on_message__()
        if not ok : return ok

        # ========================================
        # cache testing/adding
        # ========================================

        if not self.cache.check(str(self.msg.checksum),self.msg.url.path,self.msg.partstr):
            self.msg.report_publish(304,'Not modified')
            self.logger.debug("Ignored %s" % (self.msg.notice))
            return True

        self.logger.debug("Added %s" % (self.msg.notice))

        # announcing the first and unique message

        self.__on_post__()
        self.msg.report_publish(201,'Published')

        return True


    def run(self):

        # present basic config

        self.logger.info("sr_winnow run")

        # loop/process messages

        self.connect()

        while True :
              try  :
                      #  is it sleeping ?
                      if not self.has_vip() :
                         self.logger.debug("sr_winnow does not have vip=%s, is sleeping", self.vip)
                         time.sleep(5)
                         continue
                      else:
                         self.logger.debug("sr_winnow is active on vip=%s", self.vip)

                      #  heartbeat
                      ok = self.heartbeat_check()

                      #  consume message
                      ok, self.msg = self.consumer.consume()
                      self.logger.debug("sr_winnow consume, ok=%s" % ok)
                      if not ok : continue

                      #  process message (ok or not... go to the next)
                      ok = self.process_message()

              except:
                      (stype, svalue, tb) = sys.exc_info()
                      self.logger.error("Type: %s, Value: %s,  ..." % (stype, svalue))

    def reload(self):
        self.logger.info("%s reload" % self.program_name)
        self.close()
        self.configure()
        self.run()

    def start(self):
        self.logger.info("%s %s start" % (self.program_name, sarra.__version__) )
        self.run()

    def stop(self):
        self.logger.info("%s stop" % self.program_name)
        self.close()
        os._exit(0)

    def cleanup(self):
        self.logger.info("%s cleanup" % self.program_name)

        # on consuming host, do cleanup

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.cleanup()

        # on posting host
       
        self.post_hc = self.consumer.hc
        if self.post_broker :
           self.post_hc = HostConnect( self.logger )
           self.post_hc.set_url(self.post_broker)
           self.post_hc.connect()

        self.declare_exchanges(cleanup=True)

        self.close()
        os._exit(0)

    def declare(self):
        self.logger.info("%s declare" % self.program_name)

        # on consuming host, do setup

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.declare()

        # on posting host
       
        self.post_hc = self.consumer.hc
        if self.post_broker :
           self.post_hc = HostConnect( self.logger )
           self.post_hc.set_url(self.post_broker)
           self.post_hc.connect()

        self.declare_exchanges()

        self.close()
        os._exit(0)

    def declare_exchanges(self, cleanup=False):

        # define post exchange (splitted ?)

        exchanges = []

        if self.post_exchange_split != 0 :
           for n in list(range(self.post_exchange_split)) :
               exchanges.append(self.post_exchange + "%02d" % n )
        else :
               exchanges.append(self.post_exchange)

        # do exchange setup
              
        for x in exchanges :
            if cleanup: self.post_hc.exchange_delete(x)
            else      : self.post_hc.exchange_declare(x)

    def setup(self):
        self.logger.info("%s setup" % self.program_name)

        # on consuming host, do setup

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.setup()

        # on posting host
       
        self.post_hc = self.consumer.hc
        if self.post_broker :
           self.post_hc = HostConnect( self.logger )
           self.post_hc.set_url(self.post_broker)
           self.post_hc.connect()

        self.declare_exchanges()

        self.close()
        os._exit(0)
                 
# ===================================
# MAIN
# ===================================

def main():

    args,action,config,old = startup_args(sys.argv)

    winnow = sr_winnow(config,args)

    if old :
       winnow.logger.warning("Should invoke : %s [args] action config" % sys.argv[0])

    if   action == 'foreground' : winnow.foreground_parent()
    elif action == 'reload'     : winnow.reload_parent()
    elif action == 'restart'    : winnow.restart_parent()
    elif action == 'start'      : winnow.start_parent()
    elif action == 'stop'       : winnow.stop_parent()
    elif action == 'status'     : winnow.status_parent()

    elif action == 'cleanup'    : winnow.cleanup()
    elif action == 'declare'    : winnow.declare()
    elif action == 'setup'      : winnow.setup()

    else :
           winnow.logger.error("action unknown %s" % action)
           sys.exit(1)

    sys.exit(0)

# =========================================
# direct invocation
# =========================================

if __name__=="__main__":
   main()
