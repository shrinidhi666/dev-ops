#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import multiprocessing
import time
import sys
import os
import simplejson
import zmq
import uuid
import socket
import requests

if(sys.platform.lower().find("linux") >= 0):
  import setproctitle

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug
import lib.constants
import lib.config
import lib.slave_utils
import threading
import simplejson
import requests


class publisher(object):
  def __init__(self,context=None):
    if (not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._socket_pub = None
    self._socket_rep = None
    self._port = lib.config.master_conf['slave_port']
    self._start()

  def _start(self):
    self._socket_rep = self._context.socket(zmq.REP)
    self._socket_rep.setsockopt(zmq.RCVTIMEO, 1000 * 2)
    self._socket_rep.bind("tcp://*:" + str(lib.config.master_conf['master_ping_port']))
    self._socket_pub = self._context.socket(zmq.PUB)
    self._socket_pub.sndhwm = 100000
    self._socket_pub.bind("tcp://*:{0}".format(self._port))

  def publish(self, topic, state_name, request_id=None):
    if(not request_id):
      request_id = uuid.uuid4()

    lib.debug.debug("pinging : "+ str(topic) +" : "+ str(state_name))
    state_name = state_name.strip()
    if(state_name == "ping.slaveconst"):
      self._socket_pub.send_multipart([bytes(unicode(topic)), bytes(unicode(request_id)), bytes(unicode("ping.slaveconst"))])
    else:
      self._socket_pub.send_multipart([bytes(unicode(topic)), bytes(unicode(request_id)), bytes(unicode("ping.wtf"))])
    hosts_in_topic = {}
    try:
      try:
        (request_id_rep, state_name_rep, topic_rep, msg_rep) = self._socket_rep.recv_multipart()
        self._socket_rep.send_multipart([request_id_rep, state_name, msg_rep])
        lib.debug.debug(msg_rep)
      except:
        lib.debug.error(str(topic) + " : Timeout processing auth request")
        hosts_in_topic[str(topic)] = "timeout"
        return (hosts_in_topic)

      msg_reved = simplejson.loads(msg_rep)
      if (state_name == "ping.slaveconst"):
        hosts_in_topic[msg_reved['hostid']] = msg_reved['slaveconst']
      else:
        if(msg_reved['status'] == "free"):
          hosts_in_topic[msg_reved['hostid']] = msg_reved['status']
          if (state_name != "ping.wtf" and state_name != "ping.slaveconst"):
            self._socket_pub.send_multipart([bytes(unicode(topic)), bytes(unicode(request_id)), bytes(unicode(state_name))])
            hosts_in_topic[msg_reved['hostid']] = "success"
        else:
          hosts_in_topic[msg_reved['hostid']] = msg_reved['status'] +" : "+ msg_reved['request_id']
    except:
      lib.debug.error(str(state_name) + " : "+ str(request_id) +" : "+ str(sys.exc_info()))
      hosts_in_topic[msg_reved['hostid']] = str(state_name) + " : " + str(request_id) + " : " + str(sys.exc_info())

    return(hosts_in_topic)



  def __del__(self):
    try:
      self._socket_pub.close()
    except:
      lib.debug.warn(str(sys.exc_info()))
    try:
      self._socket_rep.close()
    except:
      lib.debug.warn(str(sys.exc_info()))
    try:
      self._context.term()
    except:
      lib.debug.warn(str(sys.exc_info()))





class subscriber(object):
  def __init__(self,context=None,topic="0",q=None):
    if (not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._q = q
    self._socket_sub = None
    self._socket_req = None
    self._topic = topic
    self._ip = socket.gethostbyname(lib.config.slave_conf['master'])
    self._port = lib.config.slave_conf['slave_port']
    lib.debug.debug("connecting to : "+ str(self._ip) +" : "+ str(self._port))
    self._start()

  def process(self, topic, request_id,state_name):
    return state_name

  def _fire_start_event(self):
    time.sleep(2)
    event_data = {}
    slaveconst = lib.slave_utils.slaveconst().slaveconst()
    event_data['id'] = "/devops/slave/started"
    slaveconst['event'] = event_data
    try:
      r = requests.post("http://" + lib.config.slave_conf['master'] + ":" + str(lib.config.slave_conf['master_rest_port']) + "/event", data=simplejson.dumps(slaveconst))
      r_content = r.content
      lib.debug.debug(r_content)
    except:
      lib.debug.warn(str(sys.exc_info()))


  def _start(self):
    self._start_sub()


  def _start_sub(self):
    self._socket_sub = self._context.socket(zmq.SUB)

    self._socket_sub.connect("tcp://{0}:{1}".format(self._ip, self._port))
    if(isinstance(self._topic,list)):
      for topix in self._topic:
        self._socket_sub.setsockopt(zmq.SUBSCRIBE, bytes(unicode(topix)))
        lib.debug.debug("connecting to topic : "+ str(topix))
    else:
      self._socket_sub.setsockopt(zmq.SUBSCRIBE, bytes(unicode(self._topic)))
      lib.debug.debug("connecting to topic : " + str(self._topic))
    fse = threading.Thread(target=self._fire_start_event)
    fse.start()
    while (True):
      try:
        (topic, request_id, state_name) = self._socket_sub.recv_multipart()
        if(state_name == "ping.wtf"):
          lib.debug.debug("got ping.wtf priority msg!")
          msg = {}
          if(os.path.exists(lib.constants.s_process_lock_file)):
            msg = simplejson.loads(open(lib.constants.s_process_lock_file,"r").read())
            msg['status'] = "running"
          else:
            msg['status'] = "free"
          msg['hostid'] = lib.slave_utils.hostid()
          msg_to_send = simplejson.dumps(msg)
          self._socket_req = self._context.socket(zmq.REQ)
          self._socket_req.setsockopt(zmq.SNDTIMEO, 1000)
          self._socket_req.setsockopt(zmq.RCVTIMEO, 1000*2)
          self._socket_req.connect("tcp://{0}:{1}".format(lib.config.slave_conf['master'], lib.config.slave_conf['master_ping_port']))
          try:
            self._socket_req.send_multipart([bytes(unicode(request_id)), bytes(unicode(state_name)),bytes(unicode(topic)), bytes(unicode(msg_to_send))])
          except:
            lib.debug.error(sys.exc_info())
          try:
            (request_id_recved) = self._socket_req.recv_multipart()
          except:
            lib.debug.error(sys.exc_info())

          self._socket_req.close()
        elif(state_name == "ping.slaveconst"):
          lib.debug.debug("got ping.slaveconst priority msg!")
          msg = {}
          if (os.path.exists(lib.constants.s_process_lock_file)):
            msg = simplejson.loads(open(lib.constants.s_process_lock_file, "r").read())
            msg['status'] = "running"
          else:
            msg['status'] = "free"

          msg['hostid'] = lib.slave_utils.hostid()
          msg['slaveconst'] = lib.slave_utils.slaveconst().slaveconst()

          msg_to_send = simplejson.dumps(msg)
          self._socket_req = self._context.socket(zmq.REQ)
          self._socket_req.setsockopt(zmq.SNDTIMEO, 1000)
          self._socket_req.setsockopt(zmq.RCVTIMEO, 1000)
          self._socket_req.connect("tcp://{0}:{1}".format(lib.config.slave_conf['master'], lib.config.slave_conf['master_ping_port']))
          try:
            self._socket_req.send_multipart([bytes(unicode(request_id)), bytes(unicode(state_name)), bytes(unicode(topic)), bytes(unicode(msg_to_send))])
          except:
            lib.debug.error(sys.exc_info())
          try:
            (request_id_recved) = self._socket_req.recv_multipart()
          except:
            lib.debug.error(sys.exc_info())

          self._socket_req.close()
        else:
          lib.debug.info ("{0} : {1} : {2}".format(topic,request_id,state_name))
          lib.debug.info("writing process lock file : "+ lib.constants.s_process_lock_file)
          slf = open(lib.constants.s_process_lock_file,"w")
          state_running = {}
          state_running['request_id'] = request_id
          state_running['state'] = state_name
          slf.write(simplejson.dumps(state_running))
          slf.flush()
          slf.close()
          lib.debug.info("staring process thread")
          process_thread = threading.Thread(target=self.process, args=(topic, request_id, state_name,))
          process_thread.start()
      # except KeyboardInterrupt:
      #   break
      except SystemExit:
        break
      except:
        lib.debug.error(sys.exc_info())

  def __del__(self):
    try:
      self._socket_req.close()
    except:
      lib.debug.warn(str(sys.exc_info()))
    try:
      self._socket_sub.close()
    except:
      lib.debug.warn(str(sys.exc_info()))
    try:
      self._context.term()
    except:
      lib.debug.warn(str(sys.exc_info()))





class server(object):
  def __init__(self,context=None):
    if(not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._port = lib.config.master_conf['master_ping_port']


  def process(self,received):
    return (received)


  def _worker(self,worker_url, worker_id=uuid.uuid4()):
    if (sys.platform.lower().find("linux") >= 0):
      setproctitle.setproctitle("server-worker")
    lib.debug.info (worker_url)
    context = zmq.Context()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)
    socket.poll(timeout=1)
    socket.connect(worker_url)

    while True:
      (request_id_rep, state_name_rep, topic_rep, msg_rep) = socket.recv_multipart()
      rep_sock.send_multipart([request_id_rep, state_name, msg_rep])
      lib.debug.debug(msg_rep)
      try:
        msg_reved = simplejson.loads(msg_rep)
        if (msg_reved['status'] == "free"):
          hosts_recieved[msg_reved['hostid']] = msg_reved
          lib.debug.debug("sending state : " + state_name_rep + " : ")
        else:
          return (msg_reved['status'] + " : " + msg_reved['request_id'])
      except:
        lib.debug.error(str(state_name) + " : " + str(request_id) + " : " + str(sys.exc_info()))
        return (str(state_name) + " : " + str(request_id) + " : " + str(sys.exc_info()))

    while True:
      received = socket.recv_multipart()
      lib.debug.info("Received request: [ {0} ] -> [ {1} ]".format(str(worker_id),msg_type_args))
      reply = self.process(received)
      reply_to_send = simplejson.dumps(reply)
      socket.send_multipart([bytes(unicode(hostid)),bytes(unicode(request_id)),bytes(unicode(reply_to_send))])
      lib.debug.info("Replied to request: [ {0} ] -> [ {1} ]".format(str(worker_id), msg_type_args))


  def start(self, pool_size=2):
    worker_port = 55999
    server_port = self._port
    if (sys.platform.lower().find("linux") >= 0):
      setproctitle.setproctitle("server-server")
    url_worker = "tcp://127.0.0.1:{0}".format(worker_port)
    url_client = "tcp://*:{0}".format(server_port)
    clients = self._context.socket(zmq.ROUTER)
    try:
      clients.bind(url_client)
    except:
      lib.debug.info (sys.exc_info())
      self._context.term()
      sys.exit(1)

    # Socket to talk to workers
    workers = self._context.socket(zmq.DEALER)
    try:
      workers.bind(url_worker)
    except:
      lib.debug.info (sys.exc_info())
      self._context.term()
      sys.exit(1)

    # Launch pool of worker process
    p = multiprocessing.Pool(processes=pool_size, initializer=self._worker, initargs=(url_worker,))

    zmq.proxy(clients, workers)

    # We never get here but clean up anyhow
    clients.close()
    workers.close()
    self._context.term()



class client(object):
  def __init__(self,ip='localhost',port=55555):
    self._ip = ip
    self._port = port


  def process(self, message_type,message_type_args,hostdetails):
    return message_type_args


  def send(self, message_type=None, message_type_args={}, request_id=None):
    if(not request_id):
      request_id = uuid.uuid4()
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{0}:{1}".format(self._ip, self._port))
    socket.poll(timeout=1)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    lib.debug.info("Sending request {0} …".format(request_id))

    timestarted = time.time()
    hostdetails = simplejson.dumps({'hostname':lib.constants.hostname, 'ip':lib.constants.ip})
    send_msg = simplejson.dumps(self.process(message_type, message_type_args,hostdetails))
    socket.send_multipart([bytes(unicode(request_id)), bytes(unicode(hostdetails)), bytes(unicode(message_type)), bytes(unicode(send_msg))])
    while(True):
      sockets = dict(poller.poll(10000))
      if(sockets):
        for s in sockets.keys():
          if(sockets[s] == zmq.POLLIN):
            try:
              (recv_id, recv_hostdetails, recv_msg_type, recved_msg) = s.recv_multipart()
              recv_message = self.process(recv_msg_type, recved_msg,recv_hostdetails)
              lib.debug.info("Received reply %s : %s [ %s ]" % (recv_id, recv_message, time.time() - timestarted))
            except:
              lib.debug.info (sys.exc_info())
            break
        break
      lib.debug.info ("Reciever Timeout error : Check if the server is running")



    socket.close()
    context.term()


if __name__ == "__main__":
  s = server()
  s.start()
