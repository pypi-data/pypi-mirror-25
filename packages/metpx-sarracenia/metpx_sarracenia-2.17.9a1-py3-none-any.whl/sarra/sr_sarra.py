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
# sr_sarra.py : python3 program allowing users to listen and download product from
#               another sarracenia server or from user posting (sr_post/sr_watch)
#               and reannounce the product on the current server
#
#
# Code contributed by:
#  Michel Grenier - Shared Services Canada
#  Last Changed   : Dec 22 09:20:21 EST 2015
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
#============================================================
# usage example
#
# sr_sarra [options] [config] [foreground|start|stop|restart|reload|status|cleanup|setup]
#
# sr_sarra consumes message, for each message it downloads the product
# and reannounce it. On usage of sarra is to acquire data from source
# that announce their products.  The other usage is to dessiminate products
# from other brokers/pumps.
#
# condition 1: from a source
# broker                  = where sarra is running (manager)
# exchange                = xs_source_user
# product                 = downloaded under directory (option document_root)
#                         = subdirectory from mirror option  OR
#                           message.headers['rename'] ...
#                           can be trimmed by option  strip
# post_broker             = where sarra is running (manager)
# post_exchange           = xpublic
# post_message            = same as incoming message
#                           message.headers['source']  is set from source_user
#                           message.headers['cluster'] is set from option cluster from default.conf
#                           message is built from url option give
# report_exchange            = xreport
#
#
# condition 2: from another broker/pump
# broker                  = the remote broker...
# exchange                = xpublic
# product                 = usually the product placement is mirrored 
#                           option document_root needs to be set
# post_broker             = where sarra is running (manager)
# post_exchange           = xpublic
# post_message            = same as incoming message
#                           message.headers['source']  left as is
#                           message.headers['cluster'] left as is 
#                           option url : gives new url announcement for this product
# report_exchange            = xs_"remoteBrokerUser"
#
#
#============================================================

#

import os,sys,time

try :    
         from sr_amqp           import *
         from sr_consumer       import *
         from sr_file           import *
         from sr_ftp            import *
         from sr_http           import *
         from sr_instances      import *
         from sr_message        import *
         from sr_util           import *
         print( "Using local module definitions, not system ones")
except : 
         from sarra.sr_amqp      import *
         from sarra.sr_consumer  import *
         from sarra.sr_file      import *
         from sarra.sr_ftp       import *
         from sarra.sr_http      import *
         from sarra.sr_instances import *
         from sarra.sr_message   import *
         from sarra.sr_util      import *

class sr_sarra(sr_instances):

    def __init__(self,config=None,args=None):
        sr_instances.__init__(self,config,args)

    def check(self):

        if self.broker == None :
           self.logger.error("no broker given")
           self.help()
           sys.exit(1)

        if self.exchange == None :
           self.logger.error("no exchange given")
           self.help()
           sys.exit(1)

        # bindings should be defined 

        if self.bindings == []  :
           key = self.topic_prefix + '.#'
           self.bindings.append( (self.exchange,key) )
           self.logger.debug("*** BINDINGS %s"% self.bindings)

        # make a single list for clusters that we accept message for

        #self.accept_msg_for_clusters = [ ]
        #if self.cluster:
        #    self.accept_msg_for_clusters.extend ( self.cluster )

        #if self.cluster_aliases:
        #    self.accept_msg_for_clusters.extend ( self.cluster_aliases )

        #if self.gateway_for:
        #    self.accept_msg_for_clusters.extend ( self.gateway_for  )

        #self.logger.info("accept_msg_for_clusters %s len=%s" % ( self.accept_msg_for_clusters, len(self.accept_msg_for_clusters) ) )

        # default queue name if not given

        if self.queue_name == None :
           self.queue_name  = 'q_' + self.broker.username + '.'
           self.queue_name += self.program_name + '.' + self.config_name 

        # umask change for directory creation and chmod
        #try    : os.umask(0)
        #except : pass

    def close(self):
        self.consumer.close()
        self.post_hc.close()

        if hasattr(self,'ftp_link') : self.ftp_link.close()
        if hasattr(self,'http_link'): self.http_link.close()
        if hasattr(self,'sftp_link'): self.sftp_link.close()

    def connect(self):

        # =============
        # create message if needed
        # =============

        self.msg = sr_message(self)

        # =============
        # consumer
        # =============

        self.consumer          = sr_consumer(self)
        self.msg.report_publisher = self.consumer.publish_back()
        self.msg.report_exchange  = self.report_exchange
        self.logger.info("report_back is %s to %s@%s, exchange: %s" %
               ( self.reportback, self.broker.username, self.broker.hostname, self.msg.report_exchange ) )

        # =============
        # publisher
        # =============

        # publisher host

        self.post_hc = HostConnect( logger = self.logger )
        self.post_hc.set_url( self.post_broker )
        self.post_hc.connect()

        # publisher

        self.publisher = Publisher(self.post_hc)
        self.publisher.build()
        self.msg.publisher    = self.publisher
        self.msg.pub_exchange = self.post_exchange
        self.msg.post_exchange_split = self.post_exchange_split

        # amqp resources

        self.declare_exchanges()


    def __do_download__(self):

        self.logger.debug("downloading/copying into %s " % self.new_file)

        try :
                if   self.msg.url.scheme == 'http' :
                     if not hasattr(self,'http_link') :
                        self.http_link = http_transport()
                     return self.http_link.download(self)

                elif self.msg.url.scheme == 'ftp' :
                     if not hasattr(self,'ftp_link') :
                        self.ftp_link = ftp_transport()
                     return self.ftp_link.download(self)

                elif self.msg.url.scheme == 'sftp' :
                     try    : from sr_sftp       import sftp_transport
                     except : from sarra.sr_sftp import sftp_transport
                     if not hasattr(self,'sftp_link') :
                        self.sftp_link = sftp_transport()
                     return self.sftp_link.download(self)

                elif self.msg.url.scheme == 'file' :
                     return file_process(self)

                # user defined download scripts

                elif self.do_download :
                     return self.do_download(self)

        except :
                (stype, svalue, tb) = sys.exc_info()
                self.logger.error("Download  Type: %s, Value: %s,  ..." % (stype, svalue))
                self.msg.report_publish(503,"Unable to process")
                self.logger.error("sr_sarra: could not download")

        self.msg.report_publish(503,"Service unavailable %s" % self.msg.url.scheme)

    def help(self):
        print("Usage: %s [OPTIONS] configfile [foreground|start|stop|restart|reload|status|cleanup|setup]\n" % self.program_name )
        print("version: %s \n" % sarra.__version__ )
        print("Subscribe to download, and then Recursively Re-Announce (implements a sarracenia pump)\n")
        print("OPTIONS:")
        print("instances <nb_of_instances>      default 1")
        print("\nAMQP consumer broker settings:")
        print("\tbroker amqp{s}://<user>:<pw>@<brokerhost>[:port]/<vhost>")
        print("\t\t(MANDATORY)")
        print("\nAMQP Queue bindings:")
        print("\texchange             <name>          (MANDATORY)")
        print("\ttopic_prefix         <amqp pattern>  (default: v02.post)")
        print("\tsubtopic             <amqp pattern>  (default: #)")
        print("\t\t  <amqp pattern> = <directory>.<directory>.<directory>...")
        print("\t\t\t* single directory wildcard (matches one directory)")
        print("\t\t\t# wildcard (matches rest)")
        print("\treport_exchange         <name>          (default: xreport)")
        print("\nAMQP Queue settings:")
        print("\tdurable              <boolean>       (default: False)")
        print("\texpire               <minutes>       (default: None)")
        print("\tmessage-ttl          <minutes>       (default: None)")
        print("\nFile settings:")
        print("\taccept    <regexp pattern>           (default: None)")
        print("\tdocument_root        <document_root> (MANDATORY)")
        print("\tinplace              <boolean>       (default False)")
        print("\toverwrite            <boolean>       (default False)")
        print("\tmirror               <boolean>       (default True)")
        print("\treject    <regexp pattern>           (default: None)")
        print("\tstrip      <strip count (directory)> (default 0)")
        print("\tdo_download          <script>        (default None)")
        print("\ton_file              <script>        (default None)")
        print("\nMessage settings:")
        print("\ton_message           <script>        (default None)")
        print("\trecompute_chksum     <boolean>       (default False)")
        print("\tsource_from_exchange <boolean>       (default False)")
        print("\turl                  <url>           (MANDATORY)")
        print("\nAMQP posting broker settings:")
        print("\tpost_broker amqp{s}://<user>:<pw>@<brokerhost>[:port]/<vhost>")
        print("\t\t(default: manager amqp broker in default.conf)")
        print("\tpost_exchange        <name>          (default xpublic)")
        print("\ton_post              <script>        (default None)")
        print("DEBUG:")
        print("-debug")

    # =============
    # __on_message__
    # =============

    def __on_message__(self):
        self.logger.debug("sr_sarra __on_message__")

        # apply default to a message without a source
        ex = self.msg.exchange
        if not 'source' in self.msg.headers :
           if len(ex) > 3 and ex[:3] == 'xs_' : self.msg.headers['source'] = ex[3:].split('_')[0]
           elif self.source                   : self.msg.headers['source'] = self.source
           else                               : self.msg.headers['source'] = self.broker.username
           self.logger.debug("message missing header, set default headers['source'] = %s" % self.msg.headers['source'])

        # apply default to a message without an origin cluster
        if not 'from_cluster' in self.msg.headers :
           if self.cluster : self.msg.headers['from_cluster'] = self.cluster
           else            : self.msg.headers['from_cluster'] = self.broker.netloc.split('@')[-1] 
           self.logger.debug("message missing header, set default headers['from_cluster'] = %s" % self.msg.headers['from_cluster'])

        # apply default to a message without routing clusters
        if not 'to_clusters' in self.msg.headers :
           if self.to_clusters: self.msg.headers['to_clusters'] = self.to_clusters
           else               : self.msg.headers['to_clusters'] = self.post_broker.netloc.split('@')[-1] 
           self.logger.debug("message missing header, set default headers['to_clusters'] = %s" % self.msg.headers['to_clusters'])


        # this instances of sr_sarra runs,
        # for cluster               : self.cluster
        # alias for the cluster are : self.cluster_aliases
        # it is a gateway for       : self.gateway_for 
        # all these cluster names were put in list self.accept_msg_for_clusters
        # The message's target clusters  self.msg.to_clusters should be in
        # the self.accept_msg_for_clusters list

        # if this cluster is a valid destination than one of the "to_clusters" pump
        # will be present in self.accept_msg_for_clusters

        #ok = False

        #if len(self.accept_msg_for_clusters) > 0:
        #    for target in self.msg.to_clusters :
        #        if  not target in self.accept_msg_for_clusters :  continue
        #        ok = True
        #        break

        #    if not ok :
        #        self.logger.info("skipped message not addressed to this cluster.  Accepting messages for: %s, but this message is addressed to: %s" % ( self.accept_msg_for_clusters, self.msg.to_clusters ) )
        #        return False

        self.local_file = self.new_dir + '/' + self.new_file # FIXME, remove in 2018
        self.msg.local_file = self.local_file
        saved_file = self.local_file
        # invoke user defined on_message when provided


        for plugin in self.on_message_list :
            if not plugin(self): return False
            if ( self.msg.local_file != saved_file ): # FIXME, remove in 2018
                self.logger.warning("on_message plugins should replace self.msg.local_file, by self.new_dir and self.new_file" )
                self.new_file = os.path.basename(self.local_file)
                self.new_dir = os.path.dirname(self.local_file)

        self.logger.warning("on_message end" )
        return True

    # =============
    # __on_post__ posting of message
    # =============

    def __on_post__(self):

        self.msg.local_file = self.new_file # FIXME, remove in 2018

        # invoke on_post when provided

        for plugin in self.on_post_list:
           if not plugin(self): return False
           if ( self.msg.local_file != self.new_file ): # FIXME, remove in 2018
                self.logger.warning("on_post plugins should replace self.msg.local_file, by self.new_file" )
                self.new_file = self.msg.local_file

        ok = self.msg.publish( )

        return ok

    def overwrite_defaults(self):

        # overwrite defaults
        # the default settings in most cases :
        # sarra receives directly from sources  onto itself
        # or it consumes message from another pump
        # we cannot define a default broker exchange

        # default broker and exchange None

        self.broker   = None
        self.exchange = None
        # FIX ME  report_exchange set to NONE
        # instead of xreport and make it mandatory perhaps ?
        # since it can be xreport or xs_remotepumpUsername ?

        # in most cases, sarra downloads and repost for itself.
        # default post_broker and post_exchange are

        self.post_broker    = None
        self.post_exchange  = 'xpublic'
        if hasattr(self,'manager'):
           self.post_broker = self.manager

        # Should there be accept/reject option used unmatch are accepted

        self.accept_unmatch = True

        # most of the time we want to mirror product directory and share queue

        self.mirror         = True

    # =============
    # process message  
    # =============

    def process_message(self):

        self.logger.debug("Received %s '%s' %s" % (self.msg.topic,self.msg.notice,self.msg.hdrstr))


        #=================================
        # setting up message with sr_sarra config options
        # self.set_new     : how/where sr_subscribe is configured for that product
        # self.msg.set_new : how message settings (like parts) applies in this case
        #=================================

        self.set_new()
        self.msg.set_new(self.inplace,  self.new_dir   + '/' + self.filename, self.new_url)

        #=================================
        # now message is complete : invoke __on_message__
        #=================================

        ok = self.__on_message__()
        if not ok : return ok

        #=================================
        # delete event, try to delete and propagate message
        #=================================

        if self.msg.sumflg == 'R' :
           self.logger.debug("message is to remove %s" % self.new_file)
           try : 
                  if os.path.isfile(self.new_file) : os.unlink(self.new_file)
                  if os.path.isdir( self.new_file) : os.rmdir( self.new_file)
           except:pass
           self.msg.set_topic_url('v02.post',self.new_url)
           self.msg.set_notice_url(self.new_url,self.msg.time)
           self.__on_post__()
           self.msg.report_publish(205,'Reset Content : deleted')
           return True

        #=================================
        # link event, try to link and propagate message
        #=================================
        if self.msg.sumflg == 'L' :
           self.logger.debug("message is to link %s to %s" % self.new_file, self.msg.headers['link'] )
           ok=False
           try :
               ok = os.symlink( self.msg.headers[ 'link' ], self.new_file )
               if ok:
                  self.logger.debug("%s linked to %s " % (self.new_file, self.msg.headers[ 'link' ]) )
           except:
               self.logger.error("symlink of %s %s failed." % (self.new_file, self.msg.headers[ 'link' ]) )

           if ok:
              self.msg.set_topic_url('v02.post',self.new_url)
              self.msg.set_notice_url(self.new_url,self.msg.time)
              self.__on_post__()
              self.msg.report_publish(205,'Reset Content : linked')

           return True
        #=================================
        # prepare download 
        # make sure local directory where the file will be downloaded exists
        #=================================

        # pass no warning it may already exists
        self.logger.debug("directory %s" % self.new_dir)
        try    : os.makedirs(self.new_dir,0o775,True)
        except : pass

        #=================================
        # overwrite False, user asked that if the announced file already exists,
        # verify checksum to avoid an unnecessary download
        #=================================

        need_download = True
        if not self.overwrite and self.msg.content_should_not_be_downloaded() :
           self.msg.report_publish(304, 'not modified')
           self.logger.debug("file not modified %s " % self.new_file)

           # if we are processing an entire file... we are done
           if self.msg.partflg == '1' :  return False

           need_download = False

        #=================================
        # Attempt downloads
        #=================================

        if need_download :
           i  = 0
           while i < self.attempts : 
                 ok = self.__do_download__()
                 if ok : break
                 i = i + 1
           # could not download
           if not ok : return False

           # after download setting of sum for 'z' flag ...

           if len(self.msg.sumflg) > 2 and self.msg.sumflg[:2] == 'z,':
              self.msg.set_sum(self.msg.checksum,self.msg.onfly_checksum)
              self.msg.report_publish(205,'Reset Content : checksum')

           # onfly checksum is different from the message ???
           if not self.msg.onfly_checksum == self.msg.checksum :
              self.logger.warning("onfly_checksum %s differ from message %s" % 
                                 (self.msg.onfly_checksum, self.msg.checksum))

              # force onfly checksum  in message

              if self.recompute_chksum :
                 #self.msg.compute_local_checksum()
                 self.msg.set_sum(self.msg.sumflg,self.msg.onfly_checksum)
                 self.msg.report_publish(205,'Reset Content : checksum')

           # if the part should have been inplace... but could not

           if self.inplace and self.msg.in_partfile :
              self.msg.report_publish(307,'Temporary Redirect')

           # got it : call on_part (for all parts, a file being consider
           # a 1 part product... we run on_part in all cases)

           self.msg.local_file = self.new_file # FIXME, remove in 2018

           #if self.on_part :
           #   ok = self.on_part(self)
           for plugin in self.on_part_list :
              if not plugin(self): return False

              if ( self.msg.local_file != self.new_file ): # FIXME, remove in 2018
                  self.logger.warning("on_part plugins should replace self.local_file, by self.new_file" )
                  self.new_file = self.msg.local_file


           # running on_file : if it is a file, or 
           # it is a part and we are not running "inplace"
           # or we are running in place and it is the last part.

           if self.on_file_list :

             if (self.msg.partflg == '1') or \
                       (self.msg.partflg != '1' and ( \
                             (not self.inplace) or \
                             (self.inplace and (self.msg.lastchunk and not self.msg.in_partfile)))):

                 for plugin in self.on_file_list:
                     if not plugin(self): return False

                     if ( self.msg.local_file != self.new_file ): # FIXME, remove in 2018
                         self.logger.warning("on_part plugins should replace self.local_file, by self.new_file" )
                         self.new_file = self.msg.local_file




        #=================================
        # publish our download
        #=================================

        if self.msg.partflg != '1' :
           if self.inplace : self.msg.change_partflg('i')
           else            : self.msg.change_partflg('p')

        self.msg.set_topic_url('v02.post',self.new_url)
        self.msg.set_notice_url(self.new_url,self.msg.time)
        self.__on_post__()
        self.msg.report_publish(201,'Published')

        if self.msg.partflg == '1' : return True
      
        # if dealt with a part... and inplace, try reassemble

        if self.inplace : file_reassemble(self)

        return True


    def run(self):

        # present basic config

        self.logger.info("sr_sarra run")

        # loop/process messages

        self.connect()
        active = self.has_vip()
        if not active:
            self.logger.debug("sr_sarra does not have vip=%s, is sleeping", self.vip)
        else:
            self.logger.debug("sr_sarra is active on vip=%s", self.vip)

        while True :
              try  :
                      #  is it sleeping ?
                      if not self.has_vip():
                          if active:
                             self.logger.debug("sr_sarra does not have vip=%s, is sleeping", self.vip)
                             active=False
                          time.sleep(5)
                          continue
                      else:
                         if not active:
                             self.logger.debug("sr_sarra is active on vip=%s", self.vip)
                             active=True

                      #  heartbeat
                      ok = self.heartbeat_check()

                      #  consume message
                      ok, self.msg = self.consumer.consume()
                      if not ok : continue

                      #  process message (ok or not... go to the next)
                      ok = self.process_message()

              except:
                      (stype, svalue, tb) = sys.exc_info()
                      self.logger.error("Type: %s, Value: %s,  ..." % (stype, svalue))

    def set_new(self):

        # relative path by default mirror 

        self.rel_path = '%s' % self.msg.path

        if 'rename' in self.msg.headers :
           self.rel_path = '%s' % self.msg.headers['rename']

        # if we dont mirror force  yyyymmdd/source in front

        if not self.mirror :
           yyyymmdd = time.strftime("%Y%m%d",time.gmtime())
           self.rel_path = '%s/%s/%s' % (yyyymmdd,self.msg.headers['source'],self.msg.path)

           if 'rename' in self.msg.headers :
              self.rel_path = '%s/%s/%s' % (yyyymmdd,self.msg.headers['source'],self.msg.headers['rename'])
              self.rel_path = self.rel_path.replace('//','/')

        token = self.rel_path.split('/')
        self.filename = token[-1]

        # if strip is used... strip N heading directories

        if self.strip > 0 :
           self.rel_path = '/'.join(token[self.strip:])

        self.new_dir  = ''
        if self.document_root != None :
           self.new_dir = self.document_root 

        if len(token) > 1 :
           self.new_dir = self.new_dir + '/' + '/'.join(token[self.strip:-1])

        # Local directory (directory created if needed)

        self.new_dir  = self.new_dir.replace('//','/')
        self.new_file = self.filename
        self.new_url  = urllib.parse.urlparse(self.url.geturl() + '/' + self.rel_path)

        # we dont propagate renaming... once used get rid of it
        if 'rename' in self.msg.headers : del self.msg.headers['rename']

    def reload(self):
        self.logger.info("%s reload" % self.program_name)
        self.close()
        self.configure()
        self.run()

    def start(self):
        self.logger.info("%s %s start" % (self.program_name, sarra.__version__) )
        self.run()

    def stop(self):
        self.logger.info("%s stop" % (self.program_name) )
        self.close()
        os._exit(0)

    def cleanup(self):
        self.logger.info("%s cleanup" % self.program_name)

        # consumer

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.cleanup()

        # on posting host
       
        self.post_hc = HostConnect( logger = self.logger )
        self.post_hc.set_url( self.post_broker )
        self.post_hc.connect()
        self.declare_exchanges(cleanup=True)

        self.close()
        os._exit(0)

    def declare(self):
        self.logger.info("%s declare" % self.program_name)

        # on consuming host, do declare

        self.consumer = sr_consumer(self,admin=True)
        self.consumer.declare()

        # on posting host
       
        self.post_hc = HostConnect( logger = self.logger )
        self.post_hc.set_url( self.post_broker )
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
       
        self.post_hc = HostConnect( logger = self.logger )
        self.post_hc.set_url( self.post_broker )
        self.post_hc.connect()
        self.declare_exchanges()

        self.close()
        os._exit(0)

# ===================================
# MAIN
# ===================================

def main():

    args,action,config,old = startup_args(sys.argv)

    sarra = sr_sarra(config,args)

    if old :
       sarra.logger.warning("Should invoke : %s [args] action config" % sys.argv[0])

    if   action == 'foreground' : sarra.foreground_parent()
    elif action == 'reload'     : sarra.reload_parent()
    elif action == 'restart'    : sarra.restart_parent()
    elif action == 'start'      : sarra.start_parent()
    elif action == 'stop'       : sarra.stop_parent()
    elif action == 'status'     : sarra.status_parent()

    elif action == 'cleanup'    : sarra.cleanup()
    elif action == 'declare'    : sarra.declare()
    elif action == 'setup'      : sarra.setup()

    else :
           sarra.logger.error("action unknown %s" % action)
           self.help()
           sys.exit(1)

    sys.exit(0)



# =========================================
# direct invocation
# =========================================

if __name__=="__main__":
   main()
