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
# sr_report.py : python3 program allowing users to receive all report messages
#             generated from his products
#
#
# Code contributed by:
#  Michel Grenier - Shared Services Canada
#  Last Changed   : Sep 22 10:41:32 EDT 2015
#  Last Revision  : Sep 22 10:41:32 EDT 2015
#  Last Revision  : Apr 19 13:20:00 CDT 2016
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

import signal

#============================================================
# usage example
#
# sr_report -b broker

#============================================================

try :    
         from sr_consumer        import *
         from sr_instances       import *
         from sr_util            import *
except : 
         from sarra.sr_consumer  import *
         from sarra.sr_instances import *
         from sarra.sr_util      import *


class sr_report(sr_instances):

    def __init__(self,config=None,args=None):
        #start debug before it is set by args or config option
        #self.debug = True
        #self.setlog()
        sr_instances.__init__(self,config,args)

    def check(self):
        self.nbr_instances = 1

        if self.broker == None :
           self.logger.error("no broker given")
           sys.exit(1)

        if self.exchange == None:
             if self.broker.username in self.users.keys():
                  if self.users[self.broker.username] == 'feeder' or self.users[self.broker.username] == 'admin':
                       self.exchange = 'xreport'
                  else:
                       self.exchange = 'xr_' + self.broker.username
             else:
                self.exchange = 'xr_' + self.broker.username

        if self.bindings == [] :
           key = self.topic_prefix + '.' + self.subtopic
           self.bindings     = [ (self.exchange,key) ]
        else :
           for i,tup in enumerate(self.bindings):
               e,k   = tup
               if e != self.exchange :
                  self.logger.info("exchange forced to %s" % self.exchange)
                  e = self.exchange
               self.bindings[i] = (e,k)

        # pattern must be used
        # if unset we will accept unmatched... so everything

        self.use_pattern          = self.masks != []
        self.accept_unmatch       = self.masks == []

    def close(self):
        self.consumer.close()

    def overwrite_defaults(self):
        self.broker               = None
        self.topic_prefix         = 'v02.report'
        self.subtopic             = '#'

    def help(self):
        print("Usage: %s [OPTIONS] configfile [foreground|start|stop|restart|reload|status|cleanup|setup]\n" % self.program_name )
        print("version: %s \n" % sarra.__version__ )
        print("Or   : %s [OPTIONS] -b <broker> [foreground|start|stop|restart|reload|status|cleanup|setup]\n" % self.program_name )
        self.logger.info("OPTIONS:")
        self.logger.info("-b   <broker>   default:amqp://guest:guest@localhost/")

    # =============
    # __on_message__  internal message validation
    # =============

    def __on_message__(self):
        self.logger.debug("sr_report __on_message__")

        self.logger.debug("Received topic   %s" % self.msg.topic)
        self.logger.debug("Received notice  %s" % self.msg.notice)
        self.logger.debug("Received headers %s\n" % self.msg.hdrstr)

        # user provided an on_message script

        for plugin in self.on_message_list :
            if not plugin(self): return False

        return True


    def run(self):

        self.logger.info("sr_report run")

        parent        = self
        self.consumer = sr_consumer(parent)

        #
        # loop on all message
        #

        while True :

          try  :
                 #  is it sleeping ?
                 if not self.has_vip() :
                     self.logger.debug("sr_report does not have vip=%s, is sleeping", self.vip)
                     time.sleep(5)
                     continue
                 else:
                     self.logger.debug("sr_report is active on vip=%s", self.vip)

                 #  heartbeat
                 ok = self.heartbeat_check()

                 ok, self.msg = self.consumer.consume()
                 if not ok : continue

                 ok = self.__on_message__()

          except :
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

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.cleanup()
        self.close()
        os._exit(0)

    def declare(self):
        self.logger.info("%s declare" % self.program_name)

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.declare()
        self.close()
        os._exit(0)

    def setup(self):
        self.logger.info("%s setup" % self.program_name)

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.setup()
        self.close()
        os._exit(0)
                 
# ===================================
# MAIN
# ===================================

def main():

    args,action,config,old = startup_args(sys.argv)

    # config is optional so check the argument
    if config != None:
       cfg = sr_config()
       cfg.defaults()
       cfg.general()
       ok,config = cfg.config_path('report',config,mandatory=False)
       if not ok :
          args.append(config)
          config = None

    srreport = sr_report(config,args)

    if old :
       srreport.logger.warning("Should invoke : %s [args] action config" % sys.argv[0])

    if   action == 'foreground': srreport.foreground_parent()
    elif action == 'reload'    : srreport.reload_parent()
    elif action == 'restart'   : srreport.restart_parent()
    elif action == 'start'     : srreport.start_parent()
    elif action == 'stop'      : srreport.stop_parent()
    elif action == 'status'    : srreport.status_parent()

    elif action == 'cleanup'   : srreport.cleanup()
    elif action == 'declare'   : srreport.declare()
    elif action == 'setup'     : srreport.setup()

    else :
           srlog.logger.error("action unknown %s" % action)
           sys.exit(1)

    sys.exit(0)

# =========================================
# direct invocation
# =========================================

if __name__=="__main__":
   main()
