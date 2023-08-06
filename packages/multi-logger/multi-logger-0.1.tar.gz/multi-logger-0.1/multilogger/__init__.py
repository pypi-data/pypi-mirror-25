import logging
import inspect
import watchtower
import logging.handlers
from boto3.session import Session
import socket


class Log:
    instance = None

    def __init__(self, **kwargs):
        self.AWS_KEY = kwargs['aws_key']
        self.AWS_SECRET = kwargs['aws_secret']
        self.AWS_REGION = kwargs['aws_region']
        self.CLOUDWATCH_GROUP = kwargs['cloudwatch_group']
        self.CLOUDWATCH_STREAM = kwargs['cloudwatch_stream']
        self.LOG_LEVEL = kwargs['loge_level']
        self.Log_FILE = kwargs['logfile']
        self.MODE = kwargs['mode']

    class GetLogger:
        def __init__(self):
            s = inspect.stack()[1]
            self.module_name = inspect.getmodule(s[0]).__name__
            self.line = inspect.getlineno(s[0])
            if self.module_name == "models.exceptions":
                s = inspect.stack()[3]
                self.module_name = inspect.getmodule(s[0]).__name__
                self.line = inspect.getlineno(s[0])
                print("")

        def __formatmsg(self, msg):
            return "    <{}>  ({})    {}".format(self.module_name, self.line, msg)

        def info(self, msg):
            Log.instance.info(self.__formatmsg(msg))

        def debug(self, msg):
            Log.instance.debug(self.__formatmsg(msg))

        def error(self, msg):
            Log.instance.error(self.__formatmsg(msg))

        def critical(self, msg):
            Log.instance.critical(self.__formatmsg(msg))

        def warning(self, msg):
            Log.instance.warning(self.__formatmsg(msg))

    def getLogger(self):
        if Log.instance is not None:
            return Log.GetLogger()
        log = logging.getLogger(self.CLOUDWATCH_STREAM)
        level = {"DEBUG": logging.DEBUG,
                 "INFO": logging.INFO,
                 "WARNING": logging.WARNING,
                 "ERROR": logging.ERROR,
                 "CRITICAL": logging.CRITICAL}[self.LOG_LEVEL]
        try:
            ip = socket.gethostname()
        except Exception:
            ip = socket.getfqdn()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] {} %(message)s'.format(ip))
        log.setLevel(level)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        log.addHandler(ch)

        if self.MODE == 'prod':
            boto3_session = Session(aws_access_key_id=self.AWS_KEY,
                                    aws_secret_access_key=self.AWS_SECRET,
                                    region_name=self.AWS_REGION)

            wt = watchtower.CloudWatchLogHandler(boto3_session=boto3_session,
                                                 log_group=self.CLOUDWATCH_GROUP,
                                                 stream_name=self.CLOUDWATCH_STREAM)
            wt.setFormatter(formatter)
            log.addHandler(wt)
        else:
            fh = logging.handlers.TimedRotatingFileHandler(self.Log_FILE, 'd', 1, backupCount=3)
            fh.setFormatter(formatter)
            log.addHandler(fh)

        Log.instance = log
        return Log.GetLogger()





