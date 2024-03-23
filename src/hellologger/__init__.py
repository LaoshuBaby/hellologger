import os

import logging.config

import loguru

LOG_PATH = "YOUR_HOME"


def get_logger(log_path: str, log_target:dict):
    logging_config = {
        "version": 1,
        "formatters": {
            "rawformatter": {
                "class": "logging.Formatter",
                "format": "%(message)s",
            }
        },
        "handlers": {
            "sls_handler": {
                "()": "aliyun.log.QueuedLogHandler",
                "level": "INFO",
                "formatter": "rawformatter",
                "end_point": "cn-qingdao.log.aliyuncs.com",
                "access_key_id": os.environ.get("ALIYUN_ACCESSKEY_ID"),
                "access_key": os.environ.get("ALIYUN_ACCESSKEY_SECRET"),
                "project": "yuhenglog",
                "log_store": "dev",
            }
        },
        "loggers": {
            "sls": {
                "handlers": [
                    "sls_handler",
                ],
                "level": "INFO",
                "propagate": False,
            }
        },
    }
    logging.config.dictConfig(logging_config)
    logging_handler_aliyun = logging.getLogger("sls").handlers[0]

    loguru_config = {}
    loguru_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
    logger = loguru.logger

    # for pytest project may need to record logs write by framework
    # pytest-loguru



    if log_path==None or isinstance(log_path, str)==False:
        log_path=LOG_PATH

    # local-file
    logger.add(
        sink=os.path.join(log_path, "log", "log_{time}.log"),
        format=loguru_format,
        level="TRACE",
        **loguru_config
    )
    # saas_aliyun_sls
    if log_target.get("aliyun",False):
        logger.add(
            sink=logging_handler_aliyun,
            format=loguru_format,
            level="INFO",
            **loguru_config
        )
    # saas_aws_cloudwatch
    # logger.add(sink=logging_handler_aws) # WIP
    # clickhouse
    # logger.add(sink=logging_handler_clickhouse) # WIP
    # elasticsearch
    # logger.add(sink=logging_handler_elasticsearch) # WIP
    # syslog stream
    # # Read https://docs.render.com/log-streams#sumo-logic
    # webhook
    # # discord/slack/telegram_bot, using loguru-discord
        
    def get_logger_status()->str:
        return ""

    logger.success("hellologger enabled"+get_logger_status())
    return logger

def main():
    print("Sorry, this package is not intended to run directly.")

if __name__ == "__main__":
    main()