import logging
import graypy

from balebot.config import Config


class Logger:
    logger = None

    @staticmethod
    def init_logger():

        use_graylog = Config.use_graylog
        graylog_host = Config.graylog_host
        graylog_port = Config.graylog_port
        log_level = Config.log_level
        log_facility_name = Config.log_facility_name

        temp_logger = logging.getLogger(log_facility_name)
        temp_logger.setLevel(log_level)

        if use_graylog and graylog_host and graylog_port is not None and isinstance(graylog_port, int):
            handler = graypy.GELFHandler(graylog_host, graylog_port)
        else:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s  %(filename)s:%(lineno)d  %(levelname)s:\n"%(message)s"'
            )
            handler.setFormatter(formatter)
        temp_logger.addHandler(handler)

        Logger.logger = temp_logger
        return Logger.logger

    @staticmethod
    def get_logger():
        if Logger.logger:
            return Logger.logger
        else:
            return Logger.init_logger()
