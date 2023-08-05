# -*- coding:utf-8 -*-
import time
import Queue

import gevent

from tools import now
from wechatbot import q
from ping import MyBot


bot = MyBot()


def worker():
    while True:
        bot.sync_host_check()
        check_time = now()
        bot.sync_check()
        msg = bot.sync()
        bot.handle_msg(msg)
        check_time = now() - check_time
        if check_time < 1:
            time.sleep(1 - check_time)
            bot.save_snapshot()
            gevent.sleep(0)
        continue
    gevent.sleep(0)


def chat():
    while True:
        try:
            msg = q.get(timeout=1)
        except Queue.Empty:
            gevent.sleep(0)
        content, username = msg.split("$send_to$")
        bot.send_msg_to_friend(content, username)


if __name__ == '__main__':
    bot.login_wechat()
    gevent.joinall([gevent.spawn(worker), gevent.spawn(chat)])

