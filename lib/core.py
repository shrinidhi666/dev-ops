#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import multiprocessing
import time
import sys
import simplejson
import zmq
import uuid

class publisher(object):
  def __init__(self,context=None):
    if (not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._socket = None
    self._start()

  def _start(self,pub_port=5566):
    self._context = zmq.Context()
    self._socket = self._context.socket(zmq.PUB)
    self._socket.bind("tcp://*:{0}".format(pub_port))

  def publish(self,topic="0",message={}):
    self._socket.send("{0}__{1}".format(topic,message))



class subscriber(object):
  def __init__(self,context=None,topic="0",ip="127.0.0.1",port=5566):
    if (not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._socket = None
    self._topic = topic
    self._ip = ip
    self._port = port
    self._start()


  def _start(self):
    self._context = zmq.Context()
    self._socket = self._context.socket(zmq.SUB)
    self._socket.connect("tcp://{0}:{1}".format(self._ip,self._port))
    self._socket.setsockopt(zmq.SUBSCRIBE, self._topic)
    while (True):
      string = self._socket.recv()
      (topic, messagedata) = string.split("__")
      print (topic,messagedata)
      retmsg = self.process(messagedata)
      print (retmsg)




  def process(self,msg):
    return msg





class server(object):
  def __init__(self,context=None):
    if(not context):
      self._context = zmq.Context()
    else:
      self._context = context


  def process(self, msg):
    return msg


  def _worker(self,worker_url, worker_id=uuid.uuid4()):
    print (worker_url)
    # context = zmq.Context()
    # Socket to talk to dispatcher
    socket = self._context.socket(zmq.REP)
    socket.poll(timeout=1)
    socket.connect(worker_url)

    while True:
      string = socket.recv()

      print("Received request: [ {0} ] -> [ {1} ]".format(str(worker_id),string))

      # do some 'work'
      time.sleep(1)
      reply = self.process(string)

      # send reply back to client
      socket.send(reply)


  def start(self, worker_port=5599, server_port=5555, pool_size=2):
    url_worker = "tcp://127.0.0.1:{0}".format(worker_port)
    url_client = "tcp://*:{0}".format(server_port)

    # Prepare our context and sockets
    # context = zmq.Context()

    # Socket to talk to clients
    clients = self._context.socket(zmq.ROUTER)
    try:
      clients.bind(url_client)
    except:
      print (sys.exc_info())
      self._context.term()
      sys.exit(1)

    # Socket to talk to workers
    workers = self._context.socket(zmq.DEALER)
    try:
      workers.bind(url_worker)
    except:
      print (sys.exc_info())
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
  def __init__(self,ip='localhost',port=5555):
    self._ip = ip
    self._port = port


  def _process_message(self,message):
    return message


  def send(self,message={},request_id=uuid.uuid4()):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{0}:{1}".format(self._ip,self._port))
    socket.poll(timeout=1)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    print("Sending request {0} …".format(request_id))
    send_msg = self._process_message(message)
    timestarted = time.time()
    socket.send(simplejson.dumps(message))
    try:
      recv_message = socket.recv()
    except:
      print (sys.exc_info())

    print("Received reply %s [ %s ]" % (recv_message, time.time() - timestarted))
    socket.close()


if __name__ == "__main__":
  s = server()
  s.start()
