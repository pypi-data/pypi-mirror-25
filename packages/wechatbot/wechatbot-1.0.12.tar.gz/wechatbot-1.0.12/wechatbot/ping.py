# -*- coding:utf-8 -*-
from wechatbot import WechatBot, send_my_msg


class MyBot(WechatBot):
    def text_reply(self, msg):
        if "ping" in msg:
            return 'pong'

if __name__ == "__main__":
    # 要发送的消息，填写你的微信名
    send_my_msg("Hello", u"孙传武")
