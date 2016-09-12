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
import socket


class publisher(object):
  def __init__(self,context=None):
    if (not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._socket = None
    self._start()

  def _start(self,pub_port=5566):
    self._socket = self._context.socket(zmq.PUB)
    self._socket.sndhwm = 100000
    self._socket.bind("tcp://*:{0}".format(pub_port))

  def publish(self,topic="0",message={},publish_id=None):

    self._socket.send_multipart([bytes(unicode(topic)),bytes(unicode(message))])
    if (publish_id != None):
      """
      Update the database tables
      """
      pass
    




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
    self._socket = self._context.socket(zmq.SUB)
    self._socket.connect("tcp://{0}:{1}".format(self._ip, self._port))
    if(isinstance(self._topic,list)):
      for topix in self._topic:
        self._socket.setsockopt(zmq.SUBSCRIBE, bytes(unicode(topix)))
    else:
      self._socket.setsockopt(zmq.SUBSCRIBE, bytes(unicode(self._topic)))
    while (True):
      (topic, messagedata) = self._socket.recv_multipart()
      # (topic, messagedata) = string.split("__")
      print (topic,messagedata)
      retmsg = self.process(unicode(messagedata))
      print (retmsg)




  def process(self,msg):
    return ("{0} : {1}".format("processed msg",msg))




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
      (id ,msg) = socket.recv_multipart()

      print("Received request: [ {0} ] -> [ {1} ]".format(str(worker_id),msg))

      # do some 'work'
      # time.sleep(1)
      reply = self.process(msg)

      # send reply back to client
      socket.send_multipart([bytes(id),bytes(reply)])
      print("Replied to request: [ {0} ] -> [ {1} ]".format(str(worker_id), msg))


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


  def process(self, message):
    return message


  def send(self,message={},request_id=uuid.uuid4()):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{0}:{1}".format(self._ip, self._port))
    socket.poll(timeout=1)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    print("Sending request {0} …".format(request_id))
    send_msg = self.process(message)
    timestarted = time.time()

    socket.send_multipart([bytes(request_id),bytes(message)])
    while(True):
      sockets = dict(poller.poll(10000))
      if(sockets):
        for s in sockets.keys():
          if(sockets[s] == zmq.POLLIN):
            try:
              (recv_id, recved_msg) = s.recv_multipart()
              recv_message = self.process(recved_msg)
            except:
              print (sys.exc_info())
            break
        break
      print ("Reciever Timeout error : Check if the server is running")


    print("Received reply %s : %s [ %s ]" % (recv_id,recv_message, time.time() - timestarted))
    socket.close()


if __name__ == "__main__":
  s = server()
  s.start()
