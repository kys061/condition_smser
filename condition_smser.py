#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Saisei Networks Inc. All rights reserved.

from datetime import datetime
import condition_smser_config
from condition_smser_config import query
from condition_smser_config import sendsms

_host = condition_smser_config._host
_user = condition_smser_config._user
_password = condition_smser_config._password
_db = condition_smser_config._db
_charset = condition_smser_config._charset
_port = condition_smser_config._port
_sender = condition_smser_config._sender
_receiver = condition_smser_config._receiver


ALARM_URL = condition_smser_config.API_URL + "alarms/?token=1&order=%3Ecreation_time&start=0&limit=10&\
select=name%2Cclass_name%2Ccondition%2Ccreation_time%2Ctarget_object_name%2Cseverity%2Cacknowledged_time%2Ccleared_time%2Curl%2Cdescription&\
format=human"

try:
    alarm_datas = query(ALARM_URL, condition_smser_config.API_USER, condition_smser_config.API_PASS)
    current_time = datetime.now()
except Exception as e:
    pass

for alarm in alarm_datas:
    alarm_time = datetime.strptime(alarm['creation_time'], "%Y-%m-%dT%H:%M:%S.%f")
    delta = current_time - alarm_time
    print ('delta : {}'.format(delta.seconds))

    if delta.seconds < 10:
        print ("{} : {}, timedelta : {}".format(alarm['condition'], alarm['creation_time'], delta.seconds))
        _msg = "{}알람 생성시간 : {}, 컨디션 이름 : {}".format(condition_smser_config._msg_header,
                                                                             alarm['creation_time'],
                                                                             alarm['condition'])
        _msg_euckr = condition_smser_config.to_euckr(_msg)
        sendsms(_host, _user, _password, _db, _charset, _port, _sender, _receiver, _msg_euckr, alarm['condition'], alarm['creation_time'], delta.seconds)
