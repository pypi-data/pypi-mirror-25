# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Ce module proclame la bonne parole de sieurs Sam et Max. Puissent-t-ils
    retrouver une totale liberté de pensée cosmique vers un nouvel age
    reminiscent.
"""

__version__ = "0.1.1"

from sibus_lib.DefaultLogger import mylogger
from sibus_lib.MessagingCore import BusElement, BusCore, MessageObject, set_zmq_interfaces
from sibus_lib.MessagingCore import PUBLISH_INTF_CLT, PUBLISH_INTF_SRV, LISTEN_INTF_CLT, LISTEN_INTF_SRV
from sibus_lib.SmartConfig import SmartConfigFile

def sibus_init(logger_name):
    cfg_data = SmartConfigFile()
    print "Config filepath: " + cfg_data.configfilepath

    SERVER_IP = cfg_data.get(["buscore", "host", ], "127.0.0.1")
    PUBLISH_PORT = cfg_data.get(["buscore", "internal_port", ], 1111)
    MESSAGE_PORT = cfg_data.get(["buscore", "port", ], 1981)

    LOG_FOLDER = cfg_data.get(["log", "log_directory", ], "/tmp/sibus")

    logger = mylogger(logger_name=logger_name, log_folder=LOG_FOLDER)
    logger.info("###### SiBus initialization ###########")
    logger.info("* Config file path: " + cfg_data.configfilepath)
    logger.info("* Log file path: " + LOG_FOLDER)
    logger.info("* Bus Core Config IP: " + SERVER_IP)
    logger.info("* Bus Core internal queue port: " + str(PUBLISH_PORT))
    logger.info("* Bus Core listening queue port: " + str(MESSAGE_PORT))

    LISTEN_INTF_SRV = "tcp://*:%s" % PUBLISH_PORT
    PUBLISH_INTF_SRV = "tcp://*:%s" % MESSAGE_PORT
    LISTEN_INTF_CLT = "tcp://%s:%s" % (SERVER_IP, MESSAGE_PORT)
    PUBLISH_INTF_CLT = "tcp://%s:%s" % (SERVER_IP, PUBLISH_PORT)

    set_zmq_interfaces(publish_intf_clt=PUBLISH_INTF_CLT,
                       publish_intf_srv=PUBLISH_INTF_SRV,
                       listen_intf_clt=LISTEN_INTF_CLT,
                       listen_intf_srv=LISTEN_INTF_SRV)

    logger.info("###### SiBus init done ###########")

    return logger, cfg_data
