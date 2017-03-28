#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Saisei Networks Inc. All rights reserved.

import pymysql
import logging
import requests
import time

################################################################################
# CONFIG
################################################################################
_host = ''
_user = ''
_password = ''
_db = ''
_charset = 'euckr'
_port =
_sender = ''
_receiver = ''
_msg_header = '[SAISEI ALARM SMSER] '
_msg_contents = 'Test Message 입니다.'
_msg_footer = '[---------]'
#
API_USER = 'admin'
API_PASS = 'admin'
API_URL = "http://localhost:5000/rest/NIBr730/configurations/running/"
################################################################################

# recorder logger setting
SCRIPT_MON_LOG_FILE = r'/var/log/condition_smser.log'

logger_condition_smser = logging.getLogger('saisei.condition.smser')
logger_condition_smser.setLevel(logging.INFO)

handler = logging.FileHandler(SCRIPT_MON_LOG_FILE)
handler.setLevel(logging.INFO)
filter = logging.Filter('saisei.condition')
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.addFilter(filter)

logger_condition_smser.addHandler(handler)
logger_condition_smser.addFilter(filter)


def to_euckr(msg):
    try:
        # to byte encoding with euc-kr, it means str in python2
        msg_euckr = unicode(msg,'utf-8').encode('euc-kr')
        # byte str that is encoded change to unicode with euc-kr,
        # it means decode to unicode with euc-kr.
        msg_euckr = unicode(msg_euckr,'euc-kr')
    except Exception as e:
        logger_condition_smser.error('error in to_euckr : {}'.format(e))
    else:
        return msg_euckr

def whatisthis(s):
    if isinstance(s, str):
        print ("ordinary string")
    elif isinstance(s, unicode):
        print ("unicode string")
    else:
        print ("not a string")

def to_unicode(s):
    if isinstance(s, str):
        value = s.decode('euc-kr')
    else:
        value = s
    return value

def to_str(s):
    if isinstance(s, unicode):
        value = s.encode('euc-kr')
    else:
        value = s
    return value

def query (url, user, password):
    try:
        resp = requests.get (url, auth = (user, password))
    except Exception as err:
        resp = None
        logger_condition_smser.error("### Got exception from requsts.get : {} ###".format(err))

    if resp:
        data = resp.json()
        return data['collection']
    else:
        logger_condition_smser.error("### requests.get returned None ###")
        logger_condition_smser.error("### requests.get retry interval 1 second (1st) ###")
        logger_condition_smser.error("### url: '{}' ###".format(url))
        time.sleep (1)
        resp = requests.get (url, auth = (user, password))

        if resp:
            data = resp.json ()
            return data ['collection']
        else:
            logger_condition_smser.error("### requests.get returned None ###")
            logger_condition_smser.error("### requests.get retry interval 1 second (1st) ###")
            logger_condition_smser.error("### url: '{}' ###".format(url))
            time.sleep (1)
            resp = requests.get (url, auth = (user, password))

            if resp:
                data = resp.json ()
                return data ['collection']
            else:
                logger_condition_smser.error("### requests.get returned None script exit ###")
                logger_condition_smser.error("### url: '{}' ###".format(url))
                return None

def sendsms(_host, _user, _password, _db, _charset, _port, _sender, _receiver, _msg_euckr, condition, creation_time, delta_seconds):
    print (_msg_euckr)
    try:
        # Connection
        connection = pymysql.connect(host=_host,
                                    user=_user,
                                    password=_password,
                                    db=_db,
                                    charset=_charset,
                                    port=_port)
    except Exception as e:
        logger_condition_smser.error("cannot connect to mysql server. check server, {}".format(e))
        pass
    # Connection Cursor
    try:
        with connection.cursor() as cursor:
        # SQL
            sqlAlarm = "INSERT INTO MSG_DATA \
            (CUR_STATE, REQ_DATE, CALL_TO, CALL_FROM, SMS_TXT, MSG_TYPE) \
            VALUES (0, NOW(), %s, %s, %s, 4);"
            cursor.execute(sqlAlarm, (_sender, _receiver, _msg_euckr))

        connection.commit()

    except Exception as e:
        logger_condition_smser.error("cannot excute sql syntax, {}".format(e))
        pass

    else:
        logger_condition_smser.info("success for sending sms, {} : {}, timedelta : {}".format(condition, creation_time, delta_seconds))

    finally:
        connection.close()
