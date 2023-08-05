# -*- coding:utf-8 -*-
import Queue
from wechatbot.bot import WechatBot

q = Queue.Queue()


def send_my_msg(content, user_name):
    q.put(content + "$send_to$" + user_name)
