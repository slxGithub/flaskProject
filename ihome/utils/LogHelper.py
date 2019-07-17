# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        '日志文件'
# Purpose:
#
# Author:      'lixs'
#
# Created:     '2013-12-27'
# Copyright:   (c) 'lixs' '2013-12-27'
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import datetime
import logging
import os
from . import TimeHelper

TYPE_SYS = "sys"
TYPE_CONN = "conn"
TYPE_EQUIP = "equip"
TYPE_ALARM = "alarm"
TYPE_TRANS = "trans"
TYPE_WEIXIN = "weixin"
TYPE_MNS = "mns"
TYPE_ADS = "ads"
TYPE_PACK = "pack"  # 包错误
TYPE_SQL = "sql"

UNPACK_ERROR = "unpack_error"
CRC_ERROR = "crc_error"
FORMAT_ERROR = "format_error"
START_OR_END_ERROR = "start_or_end_error"
EQUIP_NOT_EXIST = "equip_not_exist"
DATA_TYPE_ERROR = "data_type_error"
UNKNOWN_ERROR = "unKnow_error"

IN_ECHO = "in_echo"
IN_ECHO_ERROR = "in_echo_error"
OUT_ECHO_ERROR = "out_echo_error"

IN_DATA = "in_data"
IN_DATA_ERROR = "in_data_error"
OUT_DATA_ERROR = "out_data_error"

IN_QUERY = "in_query"
IN_QUERY_ERROR = "in_query_error"
OUT_QUERY_ERROR = "out_query_error"

IN_MOBILE = "in_mobile"
IN_MOBILE_ERROR = "in_mobile_error"
OUT_MOBILE_ERROR = "out_mobile_error"

IN_STATUS = "in_status"
IN_STATUS_ERROR = "in_status_error"

IN_WARNING = "in_warning"
IN_WARNING_ERROR = "in_warning_error"

IN_GPS = "in_gps"
IN_GPS_ERROR = "in_gps_error"

IN_ENQUIRY = "in_enquiry"
IN_ENQUIRY_ERROR = "in_enquiry_error"

OUT_WELL_DATA_ERROR = "out_well_data_error"

TRANS_ECHO_ERROR = "trans_echo_error"
TRANS_ECHO2_ERROR = "trans_echo2_error"
TRANS_DATA_ERROR = "trans_data_error"
TRANS_QUERY_ERROR = "trans_query_error"
TRANS_MOBILE_ERROR = "trans_mobile_error"

OUT_WEIXIN = "weixin"

SQL_ERROR = "sql_error"
SQL_ERROR_M = "sql_error_Many"

ADS_ERROR = "ads_error"
ADS_ERROR_FILE = "ads_error_file"
ADS_ERROR_CONTENT = "ads_error_content"
ADS_ERROR_SQL = "ads_error_sql"
ADS_ERROR_UPDATE = "ads_error_update"

PACK_EARLY_2014 = "pack_early_2014"
PACK_LATE_RECEIVE = "pack_late_receive"
PACK_EQUIP_NOTINSTALL = "pack_equip_not_install"

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = parent_dir


def log_info(log_type, log_code, log_context, log_time=None):
    data_logger, file_handler = __get_logger(log_type, log_time)

    msg = "[" + str(log_code) + "],  Context:" + str(log_context)
    data_logger.info(msg)

    # data_logger.removeHandler(ch)
    data_logger.removeHandler(file_handler)


def log_error(log_type, log_code, log_context, log_time=None):
    data_logger, file_handler = __get_logger(log_type, log_time)

    msg = "[" + str(log_code) + "],  Context:" + str(log_context)
    data_logger.error(msg)

    # data_logger.removeHandler(ch)
    data_logger.removeHandler(file_handler)


def log_warning(log_type, log_code, log_context, log_time=None):
    data_logger, file_handler = __get_logger(log_type, log_time)

    msg = "[" + str(log_code) + "],  Context:" + str(log_context)
    data_logger.warning(msg)

    # data_logger.removeHandler(ch)
    data_logger.removeHandler(file_handler)


def log_debug(log_type, log_code, log_context, log_time=None):
    data_logger, file_handler = __get_logger(log_type, log_time)

    msg = "[" + str(log_code) + "],  Context:" + str(log_context)
    data_logger.debug(msg)

    # data_logger.removeHandler(ch)
    data_logger.removeHandler(file_handler)


def __get_logger(log_type, log_time=None):
    # 判断log_time的类型
    if isinstance(log_time, datetime.datetime):
        log_time = TimeHelper.format_time(log_time, only_to_minute=False)
    elif log_time is None:
        log_time = datetime.datetime.now()
        log_time = TimeHelper.format_time(log_time, only_to_minute=False)
    year = log_time.year
    month = log_time.month
    day = log_time.day
    if not os.path.exists(log_dir + '\\Log_Files\\' + log_type):
        os.mkdir(log_dir + '\\Log_Files\\' + log_type)
    file_name = log_dir + '//Log_Files//' + log_type + '//' + str(year) + '_' + str(month) + '_' + str(day) + '.log'
    data_logger = logging.getLogger(log_type)
    data_logger.setLevel(logging.INFO)

    fh = logging.FileHandler(file_name, 'a', 'utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s')
    fh.setFormatter(formatter)
    data_logger.addHandler(fh)


    return data_logger, fh
