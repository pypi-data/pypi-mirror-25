# -*- coding:utf-8 -*-
import time
import sys
import logging
import json

from wechatbot.consts import (
    MSG,
    RED,
    GREEN,
    NC
)


def now():
    return int(time.time())


def red_alert(content):
    return MSG.format(color=RED, content=content, nc=NC)


def green_alert(content):
    return MSG.format(color=GREEN, content=content, nc=NC)


def create_logger(app_name):
    """Creates a logger for the given application.
    """
    _logger = logging.getLogger(app_name)
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    file_handler = logging.FileHandler("{}.log".format(app_name))
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    _logger.setLevel(logging.INFO)
    _logger.addHandler(stream_handler)
    _logger.addHandler(file_handler)
    return _logger


def get_username_by_name(dict, name):
    contacts = json.loads(dict)['MemberList']
    for contact in contacts:
        if contact["NickName"] == name:
            return contact['UserName']

if __name__ == '__main__':
    pass
