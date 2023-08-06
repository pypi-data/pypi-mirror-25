# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


INDUSTRY_LIST = [
    {
        'index': 1,
        'first_class': u'IT科技',
        'second_class': u'互联网/电子商务',
    }, {
        'index': 2,
        'first_class': u'IT科技',
        'second_class': u'IT软件与服务',
    }, {
        'index': 3,
        'first_class': u'IT科技',
        'second_class': u'IT硬件与设备',
    }, {
        'index': 4,
        'first_class': u'IT科技',
        'second_class': u'电子技术',
    }, {
        'index': 5,
        'first_class': u'IT科技',
        'second_class': u'通信与运营商',
    }, {
        'index': 6,
        'first_class': u'IT科技',
        'second_class': u'网络游戏',
    }, {
        'index': 7,
        'first_class': u'金融业',
        'second_class': u'银行',
    }, {
        'index': 8,
        'first_class': u'金融业',
        'second_class': u'基金|理财|信托',
    }, {
        'index': 9,
        'first_class': u'金融业',
        'second_class': u'保险',
    }, {
        'index': 10,
        'first_class': u'餐饮',
        'second_class': u'餐饮',
    }, {
        'index': 11,
        'first_class': u'酒店旅游',
        'second_class': u'酒店',
    }, {
        'index': 12,
        'first_class': u'酒店旅游',
        'second_class': u'旅游',
    }, {
        'index': 13,
        'first_class': u'运输与仓储',
        'second_class': u'快递',
    }, {
        'index': 14,
        'first_class': u'运输与仓储',
        'second_class': u'物流',
    }, {
        'index': 15,
        'first_class': u'运输与仓储',
        'second_class': u'仓储',
    }, {
        'index': 16,
        'first_class': u'教育',
        'second_class': u'培训',
    }, {
        'index': 17,
        'first_class': u'教育',
        'second_class': u'院校',
    }, {
        'index': 18,
        'first_class': u'政府与公共事业',
        'second_class': u'学术科研',
    }, {
        'index': 19,
        'first_class': u'政府与公共事业',
        'second_class': u'交警',
    }, {
        'index': 20,
        'first_class': u'政府与公共事业',
        'second_class': u'博物馆',
    }, {
        'index': 21,
        'first_class': u'政府与公共事业',
        'second_class': u'公共事业|非盈利机构',
    }, {
        'index': 22,
        'first_class': u'医药护理',
        'second_class': u'医药医疗',
    }, {
        'index': 23,
        'first_class': u'医药护理',
        'second_class': u'护理美容',
    }, {
        'index': 24,
        'first_class': u'医药护理',
        'second_class': u'保健与卫生',
    }, {
        'index': 25,
        'first_class': u'交通工具',
        'second_class': u'汽车相关',
    }, {
        'index': 26,
        'first_class': u'交通工具',
        'second_class': u'摩托车相关',
    }, {
        'index': 27,
        'first_class': u'交通工具',
        'second_class': u'火车相关',
    }, {
        'index': 28,
        'first_class': u'交通工具',
        'second_class': u'飞机相关',
    }, {
        'index': 29,
        'first_class': u'房地产',
        'second_class': u'建筑',
    }, {
        'index': 30,
        'first_class': u'房地产',
        'second_class': u'物业',
    }, {
        'index': 31,
        'first_class': u'消费品',
        'second_class': u'消费品',
    }, {
        'index': 32,
        'first_class': u'商业服务',
        'second_class': u'法律',
    }, {
        'index': 33,
        'first_class': u'商业服务',
        'second_class': u'会展',
    }, {
        'index': 34,
        'first_class': u'商业服务',
        'second_class': u'中介服务',
    }, {
        'index': 35,
        'first_class': u'商业服务',
        'second_class': u'认证',
    }, {
        'index': 36,
        'first_class': u'商业服务',
        'second_class': u'审计',
    }, {
        'index': 37,
        'first_class': u'文体娱乐',
        'second_class': u'传媒',
    }, {
        'index': 38,
        'first_class': u'文体娱乐',
        'second_class': u'体育',
    }, {
        'index': 39,
        'first_class': u'文体娱乐',
        'second_class': u'娱乐休闲',
    }, {
        'index': 40,
        'first_class': u'印刷',
        'second_class': u'印刷',
    }, {
        'index': 41,
        'first_class': u'其它',
        'second_class': u'其它',
    },
]


class TemplateMessage(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(TemplateMessage, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 模板消息接口, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277
        # 设置所属行业
        self.WECHAT_TEMPLATE_SET_INDUSTRY = self.API_DOMAIN + '/cgi-bin/template/api_set_industry'
        # 获取设置的行业信息
        self.WECHAT_TEMPLATE_GET_INDUSTRY = self.API_DOMAIN + '/cgi-bin/template/get_industry?access_token={access_token}'
        # 添加模板
        self.WECHAT_TEMPLATE_ADD_TEMPLATE = self.API_DOMAIN + '/cgi-bin/template/api_add_template'
        # 获取模板列表
        self.WECHAT_TEMPLATE_GET_ALL_PRIVATE_TEMPLATE = self.API_DOMAIN + '/cgi-bin/template/get_all_private_template?access_token={access_token}'
        # 删除模板
        self.WECHAT_TEMPLATE_DEL_PRIVATE_TEMPLATE = self.API_DOMAIN + '/cgi-bin/template/del_private_template'
        # 发送模板消息
        self.WECHAT_TEMPLATE_MESSAGE_SEND = self.API_DOMAIN + '/cgi-bin/message/template/send'

    def set_industry(self, industry_id1, industry_id2, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TEMPLATE_SET_INDUSTRY,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'industry_id1': industry_id1,
                'industry_id2': industry_id2,
            },
        )

    def get_industry(self, appid=None, secret=None, token=None, storage=None):
        return self.get(self.WECHAT_TEMPLATE_GET_INDUSTRY, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage))

    def add_template(self, template_id_short, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TEMPLATE_ADD_TEMPLATE,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'template_id_short': template_id_short,
            },
        )

    def get_all_private_template(self, appid=None, secret=None, token=None, storage=None):
        return self.get(self.WECHAT_TEMPLATE_GET_ALL_PRIVATE_TEMPLATE, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage))

    def del_private_template(self, template_id, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TEMPLATE_DEL_PRIVATE_TEMPLATE,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'template_id': template_id,
            },
        )

    def send_template_message(self, user_id, template_id, data, url=None, mini_program=None, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_TEMPLATE_MESSAGE_SEND,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'touser': user_id,
                'template_id': template_id,
                'url': url,
                'miniprogram': mini_program,
                'data': data,
            },
        )

tmpmsg = TemplateMessage()
set_industry = tmpmsg.set_industry
get_industry = tmpmsg.get_industry
add_template = tmpmsg.add_template
get_all_private_template = tmpmsg.get_all_private_template
del_private_template = tmpmsg.del_private_template
send_template_message = tmpmsg.send_template_message
