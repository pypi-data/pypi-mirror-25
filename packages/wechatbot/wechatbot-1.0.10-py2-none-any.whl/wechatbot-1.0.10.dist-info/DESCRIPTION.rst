=========================
WechatBot
=========================

.. image:: https://travis-ci.org/chuanwu/WechatBot.svg?branch=master

*WechatBot* is a wechat bot built for geeks.

=====================
 1. 快速上手
=====================


---------------------
1.1 安装
---------------------

.. code-block:: python

       pip install wechatbot

---------------------
1.2 用法
---------------------

贴上示例代码， wechatbot/ping.py。

.. code-block:: python

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


扫描二维码之后，机器人就跑起来啦。
这时，可以向机器人发送一个ping的消息来看看服务是否正常。
对了，短暂退出不需要重新扫描二维码登录哦～

========================
2. 规划
========================

接下来会把Bot做成一个更加基础的服务，只对外暴露两个模块:

- 在接受指令之后发送定制消息 [done]


- 主动向某个用户发送消息 [pending]


谢谢阅读！

**Good luck, have fun!**


