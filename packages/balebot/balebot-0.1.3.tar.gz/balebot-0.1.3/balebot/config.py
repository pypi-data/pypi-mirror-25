import logging


class Config:
    base_url = "wss://api.bale.ai/v1/bots/"
    request_timeout = 15

    use_graylog = False
    graylog_host = "127.0.0.1"
    graylog_port = 12201
    log_level = logging.DEBUG
    log_facility_name = "python_bale_bot"
