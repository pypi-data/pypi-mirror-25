# -*- coding: utf-8 -*-
import os
import io
import json
import random
import re
import thread
import time
import urllib
import pickle
import xml.dom.minidom

import qrcode
import requests

from wechatbot.exc import BotServerException, BotErrorCode
from wechatbot.tools import create_logger, red_alert, green_alert, now, get_username_by_name
from wechatbot.consts import (
    WECHAT_APP_ID,
    WECHAT_FIRST_LOGIN_URL,
    WECHAT_QR_CODE_STRING,
    WECHAT_SECONT_LOGIN_URL,
    WECHAT_BOT_RUNNING,
    WECHAT_BOT_SYNC_CHECK_URL,
    WECHAT_BOT_SYNC_URL,
    WECHAT_INIT_URL,
    UPLOAD_IMG_URL,
    WECHAT_MSG_URL,
    WECHAT_HEADERS,
    WECHAT_SEND_MSG_HEADER,
    WECHAT_CONTACT_URL
)

directory = os.path.dirname(os.path.abspath(__file__))
PKL_FILE = '{directory}/wechat.pkl'.format(directory=directory)


class WechatBot(object):
    def __init__(self):

        self.session = requests.Session()
        self.params = dict()

        self.params['uuid'] = None
        self.params['base_uri'] = None
        self.params['base_host'] = None

        self.params['skey'] = None
        self.params['sid'] = None
        self.params['uin'] = None
        self.params['pass_ticket'] = None
        self.params['device_id'] = 'e' + repr(random.random())[2:17]

        self.params['base_host'] = None
        self.params['base_request'] = None
        self.params['sync_host'] = None
        self.params['sync_key'] = None
        self.params['sync_key_str'] = None
        self.params['contacts'] = None
        self.params['reply'] = None
        self.params['myself'] = None

        self.func = None

    def read_snapshot(self):
        with open(PKL_FILE, 'r') as fp:
            self.params = pickle.load(fp)

    def save_snapshot(self):
        with open(PKL_FILE, 'w') as fp:
            pickle.dump(self.params, fp, protocol=2)

    def _get_qr_code(self):
        """
        生成微信登录二维码
        :return:
        """
        params = {
            'appid': WECHAT_APP_ID,
            'fun': 'new',
            'lang': 'zh_CN',
            '_': now() * 1000 + random.randint(1, 999),
        }
        r = self.session.get(WECHAT_FIRST_LOGIN_URL, params=params)
        r.encoding = 'utf-8'
        data = r.text
        regex = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        pm = re.search(regex, data)
        if pm:
            code = pm.group(1)
            self.params['uuid'] = pm.group(2)
            assert code == '200'
        else:
            raise BotServerException(BotErrorCode.GET_UUID_ERROR)

        img = qrcode.make(WECHAT_QR_CODE_STRING.format(self.params['uuid']))
        img_in_memory = io.BytesIO()
        img.save(img_in_memory, 'png')
        img_in_memory.seek(0)
        files = {'smfile': img_in_memory}
        resp = requests.post(UPLOAD_IMG_URL, files=files)
        qr_code_url = json.loads(resp.content)['data']['url']
        self.logger.info(red_alert(u"请打开此网页并扫描二维码：{}".format(qr_code_url)))
        img_in_memory.truncate()

    def init(self):
        """
        初始化，在login之后来获取sync key
        :return:
        """
        url = WECHAT_INIT_URL.format(base_uri=self.params['base_uri'],
                                     r=now(),
                                     pass_ticket=self.params['pass_ticket'])
        params = {
            'BaseRequest': self.params['base_request']
        }
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        self.params['sync_key'] = dic['SyncKey']
        self.params['sync_key_str'] = '|'.join([str(keyVal['Key']) + '_' + str(keyVal['Val'])
                                                for keyVal in self.params['sync_key']['List']])
        self.params['myself'] = dic['User']['UserName']
        return dic['BaseResponse']['Ret'] == 0

    def login(self, using_snap_shot=True):
        """
        登录
        :return:
        """
        self._get_qr_code() if not using_snap_shot else self.read_snapshot()

        redirect_url = None
        tip = 1

        while not redirect_url:
            url = WECHAT_SECONT_LOGIN_URL.format(tip=tip, uuid=self.params['uuid'], now=now())
            resp = self.session.get(url, headers=WECHAT_HEADERS)

            param = re.search(r'window.code=(\d+);', resp.text)
            code = param.group(1)

            if code == '201':
                tip = 0
            elif code == '200':
                redirect_urls = re.search(r'\"(?P<redirect_url>.*)\"', resp.content)
                if redirect_urls:
                    redirect_url = redirect_urls.group('redirect_url') + '&fun=new'
                    self.params['base_uri'] = redirect_url[:redirect_url.rfind('/')]
                    temp_host = self.params['base_uri'][8:]
                    self.params['base_host'] = temp_host[:temp_host.find("/")]
            elif code == '400':
                raise BotServerException(BotErrorCode.SNAPSHOT_EXPIRED)
            else:
                tip = 1

        resp = self.session.get(redirect_url)

        doc = xml.dom.minidom.parseString(resp.text.encode('utf-8'))
        root = doc.documentElement

        for node in root.childNodes:
            if node.nodeName == 'skey':
                self.params['skey'] = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                self.params['sid'] = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                self.params['uin'] = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                self.params['pass_ticket'] = node.childNodes[0].data
        if all([self.params['skey'], self.params['sid'], self.params['uin'], self.params['pass_ticket']]):
            self.params['base_request'] = {
                'DeviceID': self.params['device_id'],
                'Sid': self.params['sid'],
                'Skey': self.params['skey'],
                'Uin': self.params['uin']
            }
            self.init()
            self.save_snapshot()
            return True
        raise BotServerException(BotErrorCode.LOGIN_ERROR)

    def sync_check(self):
        """
        sync check.
        """

        params = {
            'r': now(),
            'skey': self.params['skey'],
            'sid': self.params['sid'],
            'uin': self.params['uin'],
            'deviceid': self.params['device_id'],
            'synckey': self.params['sync_key_str'],
            '_': now()
        }

        url = WECHAT_BOT_SYNC_CHECK_URL.format(sync_host=self.params['sync_host'], params=urllib.urlencode(params))

        while True:
            try:
                r = self.session.get(url, timeout=20)
                r.encoding = 'utf-8'
                data = r.text
                pm = re.search(r'window.synccheck=\{retcode:"(\d+)",selector:"(\d+)"\}', data)
                retcode = pm.group(1)
                selector = pm.group(2)
                return [retcode, selector]
            except requests.exceptions.ReadTimeout:
                # This is a normal response. Just ignore this exception.
                pass
            except:
                raise BotServerException(BotErrorCode.SYNC_CHECK_ERROR)

    def sync_host_check(self):
        for host1 in ['webpush.', 'webpush2.']:
            self.params['sync_host'] = host1 + self.params['base_host']
            try:
                code, selector = self.sync_check()
                if code == '0':
                    return True
            except Exception as e:
                self.logger.info(e)
        raise BotServerException(BotErrorCode.SYNC_HOST_CHECK_ERROR)

    def sync(self):
        url = WECHAT_BOT_SYNC_URL.format(base_uri=self.params['base_uri'],
                                         sid=self.params['sid'],
                                         skey=self.params['skey'],
                                         pass_ticket=self.params['pass_ticket'])

        params = {
            'BaseRequest': self.params['base_request'],
            'SyncKey': self.params['sync_key'],
            'rr': ~int(now())
        }
        try:
            r = self.session.post(url, data=json.dumps(params), timeout=60)
            r.encoding = 'utf-8'
            dic = json.loads(r.text)
            if dic['BaseResponse']['Ret'] == 0:
                self.params['sync_key'] = dic['SyncKey']
                self.params['sync_key_str'] = '|'.join(str(data['Key']) + '_' + str(data['Val'])
                                                       for data in self.params['sync_key']['List'])
            return dic
        except Exception:
            raise BotServerException(BotErrorCode.SYNC_ERROR)

    def proc_msg(self):

        self.sync_host_check()

        while True:
            check_time = now()
            self.sync_check()
            msg = self.sync()
            self.handle_msg(msg)
            check_time = now() - check_time
            if check_time < 1:
                time.sleep(1 - check_time)
            self.save_snapshot()

    def handle_msg(self, msgs):
        for msg in msgs["AddMsgList"]:
            if ':<br/>!' in msg['Content']:
                _, msg['Content'] = msg['Content'].split('<br/>', 1)
            try:
                response = self.text_reply(msg['Content']) if self.text_reply(msg['Content']) else ''
            except Exception as e:
                response = e.message
            self.logger.info(green_alert(unicode(msg['Content'] + " replied: " + response)))
            if not msg['Content'] or not response:
                continue
            reply = {
                'BaseRequest': self.params['base_request'],
                'Msg': {
                    'Type': 1,
                    'Content': response.decode('utf-8'),
                    'FromUserName': msg['ToUserName'],
                    'ToUserName': msg['FromUserName']
                },
                'Scene': msg['RecommendInfo']['Scene']
            }
            self.params['reply'] = reply
            try:
                self.send_msg(reply)
            except Exception as e:
                reply['Msg']['Content'] = 'error occurs: {}'.format(e)
                self.send_msg(reply)
            # send msg to someone
            # self.send_msg_to_friend("Hello", u"桃子")

    def send_msg_to_friend(self, content, user_name):

        reply = self.params['reply']
        if not reply:
            return
        reply['Msg']['FromUserName'] = self.params['myself']
        reply['Msg']['ToUserName'] = get_username_by_name(self.params['contacts'], user_name)
        reply['Msg']['Content'] = content
        self.send_msg(reply)

    def get_all_contacts(self):
        data = {
            'base_uri': self.params['base_uri'],
            'pass_ticket': self.params['pass_ticket'],
            'skey': self.params['skey'],
            'now': now()
        }
        resp = self.session.post(
            WECHAT_CONTACT_URL.format(base_uri=self.params['base_uri'], pass_ticket=self.params['pass_ticket'],
                                      skey=self.params['skey'], now=int(now())), data={},
            headers=WECHAT_SEND_MSG_HEADER)
        self.params['contacts'] = resp.content

    def send_msg(self, reply):
        url = self.params['base_uri'] + '/webwxsendmsg'
        msg_id = str(now() * 1000) + str(random.random())[:5].replace('.', '')
        reply['Msg'].update({'LocalId': msg_id, 'ClientMsgId': msg_id})
        data = json.dumps(reply, ensure_ascii=False).encode('utf-8')
        for i in range(5):
            try:
                r = self.session.post(url, data=data, headers=WECHAT_SEND_MSG_HEADER)
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                pass
            if r.status_code == 200:
                return
        raise BotServerException(BotErrorCode.SEND_MSG_ERROR)

    def text_reply(self, msg):
        """
        向特定的回应信息发送消息，请继承该方法，具体请看ping.py的实现
        :return:
        """
        pass

    def call(self, msg):
        return self.func(msg)

    @property
    def logger(self):
        """Create a logger for Bot
        """
        return create_logger(self.__class__.__name__)

    def login_wechat(self):
        try:
            self.login(using_snap_shot=True)
        except:
            self.login(using_snap_shot=False)
        self.logger.info(green_alert(WECHAT_BOT_RUNNING))
        self.get_all_contacts()

    def run(self):
        self.proc_msg()
