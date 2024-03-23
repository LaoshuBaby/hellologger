import os

import logging.config

import loguru

from .const import *


def get_variable(key=None, default=None):
    if key != None and isinstance(key, str):
        if os.environ.get(key, None):
            return os.environ.get(key, None)
    elif default != None and isinstance(default, str):
        return default
    else:
        return None


def get_logger(log_path: str, log_target: dict, log_level={}, **log_config):
    """
    log_target: 是否启用不同的数据源
    不同数据源会使用对应的数据驱动
    代号可见如下：
    * local
    * aliyun
    * aws
    """
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
                "level": log_level.get("aliyun", "INFO"),
                "formatter": "rawformatter",
                "end_point": get_variable(default=LOG_CONFIG_ALIYUN_ENDPOINT),
                "access_key_id": get_variable(
                    key="ALIYUN_ACCESSKEY_ID",
                    default=LOG_CONFIG_ALIYUN_ACCESSKEY_ID,
                ),
                "access_key": get_variable(
                    key="ALIYUN_ACCESSKEY_SECRET",
                    default=LOG_CONFIG_ALIYUN_ACCESSKEY_SECRET,
                ),
                "project": get_variable(
                    default=LOG_CONFIG_ALIYUN_PROJECT,
                ),
                "log_store": get_variable(
                    default=LOG_CONFIG_ALIYUN_LOGSTORE,
                ),
            }
        },
        "loggers": {
            "sls": {
                "handlers": [
                    "sls_handler",
                ],
                "level": log_level.get("aliyun", "INFO"),
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

    if log_path == None or isinstance(log_path, str) == False:
        log_path = LOG_PATH

    # local-file
    logger.add(
        sink=os.path.join(log_path, "log", "log_{time}.log"),
        format=loguru_format,
        level="TRACE",
        **loguru_config,
    )
    # saas_aliyun_sls
    if log_target.get("aliyun", False):
        logger.add(
            sink=logging_handler_aliyun,
            format=loguru_format,
            level="INFO",
            **loguru_config,
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
    # # discord/slack/telegram_bot, using loguru-discord  webhook需要传入配置文件，没有就默认discord的

    def get_logger_status() -> str:
        logger_status = []
        for device, status in log_config.items():
            logger_status.append(f"{device}-{status}")
        return "\n".join(logger_status)

    logger.success("hellologger enabled" + "\n" + get_logger_status())
    return logger


def main():
    print("Sorry, this package is not intended to run directly.")


if __name__ == "__main__":
    main()
