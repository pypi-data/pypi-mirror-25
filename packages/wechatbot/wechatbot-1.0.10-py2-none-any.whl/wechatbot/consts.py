# -*- coding:utf-8 -*-
ALL_KEYWORDS = 'WX_BOT_KEYWORDS'

RESERVED_COMMAND_LIST = ['help', ]

UPLOAD_IMG_URL = 'https://sm.ms/api/upload'

MSG = u'{color}{content}{nc}'

RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m'  # No Color

WECHAT_APP_ID = 'wx782c26e4c19acffb'
WECHAT_FIRST_LOGIN_URL = 'https://login.weixin.qq.com/jslogin'
WECHAT_QR_CODE_STRING = 'https://login.weixin.qq.com/l/{}'
WECHAT_SECONT_LOGIN_URL = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip={tip}&uuid={uuid}&_={now}'
WECHAT_CONTACT_URL = '{base_uri}/webwxgetcontact?pass_ticket={pass_ticket}&skey={skey}&r={now}'
WECHAT_MSG_URL = '{base_uri}/webwxsendmsg?pass_ticket={pass_ticket}'
WECHAT_BOT_SYNC_CHECK_URL = 'https://{sync_host}/cgi-bin/mmwebwx-bin/synccheck?{params}'
WECHAT_BOT_SYNC_URL = '{base_uri}/webwxsync?sid={sid}&skey={skey}&lang=en_US&pass_ticket={pass_ticket}'
WECHAT_INIT_URL = '{base_uri}/webwxinit?r={r}i&lang=en_US&pass_ticket={pass_ticket}'

WECHAT_BOT_RUNNING = u'机器人已经启动啦！你可以发送`ping`给机器人，机器人会回复哦。'

WECHAT_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'cache-control': 'max-age=0',
    'host': 'login.wx.qq.com',
    'content-type': 'application/json; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
}

WECHAT_SEND_MSG_HEADER = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'cache-control': 'max-age=0',
    'content-type': 'application/json; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
}
