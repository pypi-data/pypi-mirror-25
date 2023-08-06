# coding=utf-8
from __future__ import print_function, absolute_import


# 基本api
from gm import __version__
from gm.csdk.c_sdk import py_gmi_set_version
from .basic import (
    set_token, get_version, subscribe, unsubscribe,
    current, get_strerror, schedule, run, set_parameter,
    add_parameter, log, set_serv_addr)

# 交易api
from .trade import (
    order_target_volume, order_target_value, order_target_percent,
    order_volume, order_percent, order_value, order_batch,
    cancel_all_orders, order_cancel, order_close_all,
    get_orders, get_unfinished_orders)

# 数据查询api
from .query import (
    history_n, history, get_fundamentals, get_dividend, get_continuous_contracts, get_next_trading_date,
    get_previous_trading_date, get_trading_dates, get_concept, get_industry, get_constituents, get_history_constituents,
    get_history_instruments, get_instrumentinfos, get_instruments, get_sector
)

__all__ = [
    'order_target_volume', 'order_target_value', 'order_target_percent',
    'order_volume', 'order_percent', 'order_value', 'order_batch',
    'cancel_all_orders', 'order_cancel', 'order_close_all',
    'get_orders', 'get_unfinished_orders',

    'set_token', 'get_version', 'subscribe', 'unsubscribe',
    'current', 'get_strerror', 'schedule', 'run',
    'set_parameter', 'add_parameter', 'log',

    'history_n', 'history', 'get_fundamentals', 'get_dividend',
    'get_continuous_contracts', 'get_next_trading_date',
    'get_previous_trading_date', 'get_trading_dates', 'get_concept',
    'get_industry', 'get_constituents', 'get_history_constituents',
    'get_history_instruments', 'get_instrumentinfos',
    'get_instruments', 'get_sector', 'set_serv_addr'
]


py_gmi_set_version(__version__.__version__, 'python')
