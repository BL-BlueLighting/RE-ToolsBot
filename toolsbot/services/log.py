from datetime import datetime, timedelta
from sys import stdout

from loguru import logger as logger_
from nonebot.log import default_filter
from nonebot.log import logger as nb_logger
from nonebot.log import logger_id

from ..configs import LOG_PATH

my_format = "<g>{time:MM-DD HH:mm:ss}</g> [<lvl>{level:<7}</lvl>] <c><u>{name:<7}</u></c> | {message}"

nb_logger.remove(logger_id)

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
    filter=default_filter,
    retention=timedelta(days=30))

logger.add(
    LOG_PATH / f'error_{datetime.now().date()}.log',
    level='ERROR',
    rotation='00:00',
    format=my_format,
    filter=default_filter,
    retention=timedelta(days=30))

_info = logger.info
_warn = logger.warning
_error = logger.error
_crit = logger.critical
# 不是,你连logger都懒得打了是吗