# -*- coding:utf-8 -*-
from wechatbot import WechatBot


class MyBot(WechatBot):
    def text_reply(self, msg):
        if "ping" in msg:
            return 'pong'


if __name__ == '__main__':
    bot = MyBot()
    bot.login_wechat()
    bot.run()
