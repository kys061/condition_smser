#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Saisei Networks Inc. All rights reserved.

from datetime import datetime
import sms_sender_config
from sms_sender_config import query, sendsms, logger_condition_smser

_host = sms_sender_config._host
_user = sms_sender_config._user
_password = sms_sender_config._password
_db = sms_sender_config._db
_charset = sms_sender_config._charset
_port = sms_sender_config._port
_sender = sms_sender_config._sender
_receiver = sms_sender_config._receiver

_delta = 4000


ALARM_URL = sms_sender_config.API_URL + "alarms/?token=1&order=<creation_time&start=0&limit=10&\
select=name%2Cclass_name%2Ccondition%2Ccreation_time%2Ctarget_object_name%2Cseverity%2Cacknowledged_time%2Ccleared_time%2Curl%2Cdescription&\
format=human"

try:
    alarm_datas = query(ALARM_URL, sms_sender_config.API_USER, sms_sender_config.API_PASS)
    current_time = datetime.now()
except Exception as e:
    pass

for alarm in alarm_datas:
    alarm_time = datetime.strptime(alarm['creation_time'], "%Y-%m-%dT%H:%M:%S.%f")
    delta = current_time - alarm_time
    print (alarm)
    if delta.seconds < _delta:
        _msg = "{}알람 생성시간 : {}, 컨디션 이름 : {}".format(sms_sender_config._msg_header,
                                                                             alarm['creation_time'],
                                                                             alarm['condition'])
        _msg_euckr = sms_sender_config.to_euckr(_msg)
        logger_condition_smser.info("Condition is triggerd, condition : {}, creation_time : {}, timedelta : {}".format(alarm['condition'], alarm['creation_time'], delta.seconds))
        #sendsms(_host, _user, _password, _db, _charset, _port, _sender, _receiver, _msg_euckr, alarm['condition'], alarm['creation_time'], delta.seconds)
