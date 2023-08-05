
# -*- coding: utf-8 -*-

import logging
import os

from logging.handlers import RotatingFileHandler

LOG_DIRECTORY = "/tmp/sibus"


def mylogger(logger_name, log_folder=LOG_DIRECTORY):
    # création de l'objet logger qui va nous servir à écrire dans les logs
    logger = logging.getLogger()
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s|%(levelname)08s | %(message)s')
    stream_formatter = logging.Formatter('%(levelname)08s | %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo

    if not os.path.isdir(log_folder):
        print "Creating log directory: ", log_folder
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, logger_name + '.log')
    print "Log file: ", log_file
    file_handler = RotatingFileHandler(log_file, 'a', 1000000, 1)
    # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # création d'un second handler qui va rediriger chaque écriture de log
    # sur la console
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    steam_handler.setFormatter(stream_formatter)
    logger.addHandler(steam_handler)

    return logger