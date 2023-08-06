#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import datetime as dt
import json
import logging
import re
import socket
import threading
import time
import uuid

import zmq
from marshmallow import Schema, fields, post_load, ValidationError

from sibus_lib.utils import float_to_datetime, datetime_now_float

logger = logging.getLogger()

LISTEN_INTF_SRV = None
PUBLISH_INTF_SRV = None

LISTEN_INTF_CLT = None
PUBLISH_INTF_CLT = None


def set_zmq_interfaces(listen_intf_srv, publish_intf_srv, listen_intf_clt, publish_intf_clt):
    global LISTEN_INTF_SRV, PUBLISH_INTF_SRV, LISTEN_INTF_CLT, PUBLISH_INTF_CLT
    LISTEN_INTF_SRV = listen_intf_srv
    PUBLISH_INTF_SRV = publish_intf_srv

    LISTEN_INTF_CLT = listen_intf_clt
    PUBLISH_INTF_CLT = publish_intf_clt

###############################################################################################
###############################################################################################

class MessageSchema(Schema):
    uid = fields.Str()
    origin_host = fields.Str()
    origin_service = fields.Str()
    origin_uid = fields.Str()
    date_creation = fields.Float()
    topic = fields.Str()
    b64data = fields.Str()

    @post_load
    def make_object(self, data):
        msg = MessageObject()
        msg.date_creation = data["date_creation"]
        msg.origin_host = data["origin_host"]
        msg.origin_service = data["origin_service"]
        msg.origin_uid = data["origin_uid"]
        msg.uid = data["uid"]
        msg.topic = data["topic"]
        msg.b64data = data["b64data"]
        return msg

    def toObject(self, json_string):
        message = self.loads(json_string)
        return message.data

###############################################################################################
###############################################################################################

class MessageObject:

    def __init__(self, data=None,
                    topic="*"
                 ):
        # type: (object, object) -> object
        self.uid = str(uuid.uuid1())
        self.origin_host = socket.getfqdn()
        self.origin_service = None
        self.origin_uid = None
        self.date_creation = datetime_now_float()
        self.topic = topic
        self.set_data(data)

    def __repr__(self):
        tmp_data = self.get_data()
        if tmp_data is not None and len(tmp_data) > 2048:
            data = "long data:%d" % len(tmp_data)
        else:
            data = tmp_data

        return "<BusMessage> origin:%s.%s; topic:%s; date:%s; data:%s"%(self.origin_host, self.origin_service, self.topic,
                                                                        str(float_to_datetime(self.date_creation)),
                                                                        data)

    def set_data(self, data):
        if data is None:
            self.b64data = ""
            return
        if type(data) <> dict:
            logger.error("Data in message bus must be provided as 'dict' !!")
            self.b64data = ""
            return
        self.b64data = base64.b64encode(json.dumps(data))

    def get_data(self):
        if len(self.b64data) == 0:
            return None
        return json.loads(base64.b64decode(self.b64data))

    def toJson(self):
        schema = MessageSchema()
        json_result = schema.dumps(self)
        return json_result.data


###############################################################################################
###############################################################################################

class BusCore(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()

        # Initialize the ZeroMQ context
        self.context = zmq.Context()
        self._init_reception_queue()
        self._init_emission_queue()


    def _init_reception_queue(self):
        # Configure ZeroMQ to receive messages
        self.zmq_recv = self.context.socket(zmq.SUB)
        # The communication is made on socket 1112
        self.zmq_recv.bind(LISTEN_INTF_SRV)
        self.zmq_recv.setsockopt(zmq.SUBSCRIBE, '')  # subscribe to everything
        logger.info("Bus Core Receiving messages on "+LISTEN_INTF_SRV)

    def _init_emission_queue(self):
        # Configure ZeroMQ to send messages
        self.zmq_send = self.context.socket(zmq.PUB)
        # The communication is made on socket 1111
        self.zmq_send.bind(PUBLISH_INTF_SRV)
        logger.info("Bus Core Sending messages on "+PUBLISH_INTF_SRV)

    def publish(self, msg, from_core=False):
        """self.channel.basic_publish(exchange='',
                              routing_key=DATAQUEUE_NAME,
                              body=msg.msg())"""
        if from_core:
            msg.origin_uid = 0
            msg.origin_service = "sibus.core"
        else:
            msg.origin_uid = msg.origin_uid
            msg.origin_service = msg.origin_service
        json_result = msg.toJson()

        logger.info("Core Bus publishing message : %s"%str(msg))

        try:
            self.zmq_send.send(json_result)
        except zmq.ZMQError as err:
            logger.info("Error while trying to publish the message : %s"%str(err))
            return False

        return True

    def run(self):
        logger.info("Bus core start listening messages")
        while not self._stopevent.isSet():
            # Command to wait for an incoming message
            try:
                # Capture the message and store it
                body = self.zmq_recv.recv(zmq.NOBLOCK)
            except zmq.ZMQError as err:
                #logger.error("ZMQ Error : %s" % str(err))
                time.sleep(0.01)
                continue

            schema = MessageSchema(strict=True)
            try:
                message = schema.toObject(body)
            except ValidationError as err:
                logger.error("Invalid message format: %s, dropping it" % str(body))
                logger.error("    ERRORS: %s" % str(err.messages))
                return

            logger.debug("Bus Core received a message : %s" % str(message))

            self.publish(message)

        logger.info("Bus core stopped listening message.")

    def stop(self):
        self._stopevent.set( )
        self.zmq_send.close()
        self.zmq_recv.close()
        self.context.term()
        logger.info("Bus core cleaned and terminated. Thank you !")

##############################################################################################""

class BusElement(threading.Thread):

    def __init__(self, service_name,
                 callback=None,
                 filter=None,
                 ignore_my_msg=True):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        # Initialize the ZeroMQ context
        self.context = zmq.Context()
        self._init_reception_queue()
        self._init_emission_queue()
        self._ignore_me = ignore_my_msg

        self.registered_topics = []

        self.service_name = service_name
        self.bus_uid = str(uuid.uuid1())
        self.set_callback(callback=callback)

    def register_topic(self, topic_pattern):
        if topic_pattern == "*":
            self.registered_topics.append(topic_pattern)
        else:
            topic_pattern = topic_pattern.replace("*", ".*?")
            regex = re.compile(topic_pattern)
            self.registered_topics.append(regex)

    def set_callback(self, callback):
        self._callback = callback

    def _init_reception_queue(self):
        # Configure ZeroMQ to receive messages
        self.zmq_recv = self.context.socket(zmq.SUB)
        # The communication is made on socket 1112
        logger.info("Receiving messages on " + LISTEN_INTF_CLT)
        self.zmq_recv.connect(LISTEN_INTF_CLT)
        self.zmq_recv.setsockopt(zmq.SUBSCRIBE, '')  # subscribe to everything

    def _init_emission_queue(self):
        # Configure ZeroMQ to send messages
        self.zmq_send = self.context.socket(zmq.PUB)
        logger.info("Sending messages on " + PUBLISH_INTF_CLT)
        # The communication is made on socket 1111
        self.zmq_send.connect(PUBLISH_INTF_CLT)


    def __internal_data_cb(self, body):
        schema = MessageSchema(strict=True)
        try:
            message = schema.toObject(body)
        except ValidationError as err:
            logger.error("Invalid message format: %s, dropping it" % str(body))
            logger.error("    ERRORS: %s" % str(err.messages))
            return
        pass
        if (message.origin_uid == self.bus_uid) and self._ignore_me is True:
            #ignore message published by me !!
            return

        for topic in self.registered_topics:
            if topic == "*" or topic.match(message.topic) is not None:
                if self._callback is not None:
                    logger.debug("Message triggered: %s" % str(message))
                    self._callback(message)
                    return

    def publish(self, msg):
        """self.channel.basic_publish(exchange='',
                              routing_key=DATAQUEUE_NAME,
                              body=msg.msg())"""
        msg.origin_uid = self.bus_uid
        msg.origin_service = self.service_name
        json_result = msg.toJson()

        logger.debug("Publishing message : %s" % str(msg))

        try:
            self.zmq_send.send(json_result)
        except zmq.ZMQError as err:
            logger.error("ZMQ error trying to send message: %s" % str(err))

    def run(self):
        logger.info("Bus client start listening messages on bus")
        self.publish(MessageObject(topic="admin.start"))
        dt_start = dt.datetime.now()
        while not self._stopevent.isSet():
            # Command to wait for an incoming message
            try:
                # Capture the message and store it
                body = self.zmq_recv.recv(zmq.NOBLOCK)
                self.__internal_data_cb(body)
                #logger.debug("Message received : %s"%str(body))
            except zmq.ZMQError as err:
                #logger.error("ZMQ error message : %s" % str(err))
                continue

            time.sleep(0.01)
            dt_now = dt.datetime.now()
            if (dt_now - dt_start).seconds > 30:
                self.publish(MessageObject(topic="admin.heartbeat"))
                dt_start = dt_now

        logger.info("Bus client stopped listening messages on bus")

    def stop(self):
        self.publish(MessageObject(topic="admin.terminated"))
        time.sleep(0.5)
        self._stopevent.set( )
        self.zmq_send.close()
        self.zmq_recv.close()
        self.context.term()
        logger.info("Bus client cleaned and terminated. Thank you !")

