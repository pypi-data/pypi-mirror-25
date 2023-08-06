=====================
pywe-template-message
=====================

Wechat Template Message Module for Python.

Installation
============

::

    pip install pywe-template-message


Usage
=====

::

    from pywe_template_message import TemplateMessage, INDUSTRY_LIST, set_industry, get_industry, add_template, get_all_private_template, del_private_template, send_template_message


Method
======

::

    class TemplateMessage(BaseToken):
        def __init__(self, appid=None, secret=None, token=None, storage=None):
            super(TemplateMessage, self).__init__(appid=appid, secret=secret, token=token, storage=storage)

    def set_industry(self, industry_id1, industry_id2, appid=None, secret=None, token=None, storage=None):

    def get_industry(self, appid=None, secret=None, token=None, storage=None):

    def add_template(self, template_id_short, appid=None, secret=None, token=None, storage=None):

    def get_all_private_template(self, appid=None, secret=None, token=None, storage=None):

    def del_private_template(self, template_id, appid=None, secret=None, token=None, storage=None):

    def send_template_message(self, user_id, template_id, data, url=None, mini_program=None, appid=None, secret=None, token=None, storage=None):

