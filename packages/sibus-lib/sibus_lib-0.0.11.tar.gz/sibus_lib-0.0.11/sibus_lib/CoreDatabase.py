import logging
import threading
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sibus_lib.utils import float_to_datetime, datetime_now_float

logger = logging.getLogger()

CoreDBBase = declarative_base()

class CoreDatabase(threading.Thread):
    def __init__(self, host="127.0.0.1", port=3306, login=None, password=None, database=None):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self._sql_url = "mysql+pymysql://%s:%s@%s:%d/%s" % (login, password, host, port, database)
        self.init_db()

    def init_db(self):
        logger.info("Connecting to SQL DB on " + self._sql_url)
        engine = create_engine(self._sql_url, echo=True)
        CoreDBBase.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.SessionMaker = Session
        #self.start()

    def run(self):
        session = self.SessionMaker()
        while not self._stopevent.isSet():
            for instance in self.session.query(BusElementDB).order_by(BusElementDB.last_event_date):
                logger.info("%s.%s is %s (started:%s, last:%s)"%(instance.bus_origin_host,
                                                                 instance.bus_origin_service,
                                                                 instance.status,
                                                                 float_to_datetime(instance.first_event_date),
                                                                 float_to_datetime(instance.last_event_date)))

                if (datetime_now_float() - instance.last_event_date > 60) and (instance.status <> "dead"):
                    instance.status = "dead"
                    session.add(instance)

            session.commit()
            time.sleep(5)

    def stop(self):
        self._stopevent.set( )

    def get_session(self):
        return self.SessionMaker()

    def update_buselement(self, bus_uid, host, service, event_date):
        session = self.SessionMaker()


