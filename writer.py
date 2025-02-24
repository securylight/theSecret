import datetime
import logging

try:
    from google.cloud import ndb

    class LogEntry(ndb.Model):
        timestamp = ndb.DateTimeProperty(auto_now_add=True)
        message = ndb.StringProperty()
        response = ndb.StringProperty()
        #level = ndb.IntegerProperty(choices=list(range(1, 11)))

    def append_line_to_ndb(level, message, response):
        client = ndb.Client()
        with client.context():
            parent_key = ndb.Key("LogLevel", str(level))
            log_entry = LogEntry(parent=parent_key, message=message, response=response)
            log_entry.put()
            logging.info(f"log entry created for level {level}")
except ImportError:
    def append_line_to_ndb(level, message, response):
        # Do nothing in local development
        pass
