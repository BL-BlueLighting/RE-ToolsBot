from datetime import datetime, timedelta
from sys import stdout
from typing import TYPE_CHECKING

from loguru import logger as logger_

if TYPE_CHECKING:
    from loguru import Record

from nonebot.log import default_filter
from nonebot.log import logger as nb_logger
from nonebot.log import logger_id

from ..configs import LOG_PATH

my_format = "<g>{time:MM-DD HH:mm:ss}</g> [<lvl>{level:<7}</lvl>] <c><u>{name:<7}</u></c> | {message}"

nb_logger.remove(logger_id)

def application_filter(application:str | None = None):
    def filter(record: "Record"):
        """默认的日志过滤器，根据 `config.log_level` 配置改变日志等级。"""
        log_level = record["extra"].get("nonebot_log_level", "INFO")
        if application is not None and record["extra"].get("application") != application:
            return False
        level_no = logger.level(log_level).no if isinstance(log_level, str) else log_level
        return record["level"].no >= level_no
    return filter

logger_id = nb_logger.add(
    stdout,
    format=my_format,
    filter=default_filter
)

logger = logger_

logger.add(
    LOG_PATH / f'{datetime.now().date()}.log',
    level='INFO',
    rotation='00:00',
    format=my_format,
    filter=application_filter("toolsbot"),
    retention=timedelta(days=10))

logger.add(
    LOG_PATH / f'all_{datetime.now().date()}.log',
    level='INFO',
    rotation='00:00',
    format=my_format,
    filter=application_filter(),
    retention=timedelta(days=10))

logger.add(
    LOG_PATH / f'error_{datetime.now().date()}.log',
    level='ERROR',
    rotation='00:00',
    format=my_format,
    filter=application_filter("toolsbot"),
    retention=timedelta(days=10))

logger_bind = logger.bind(application="toolsbot")

_trace = logger_bind.trace
_debug = logger_bind.debug
_info = logger_bind.info
_warn = logger_bind.warning
_error = logger_bind.error
_crit = logger_bind.critical
_done = logger_bind.success
# 不是,你连logger都懒得打了是吗