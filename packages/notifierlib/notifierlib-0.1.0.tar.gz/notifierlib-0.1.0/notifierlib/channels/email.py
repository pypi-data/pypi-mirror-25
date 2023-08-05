#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: email.py
"""Email module file"""

from emaillib import EasySender
from notifierlib.notifierlib import Channel


__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''18-09-2017'''


class Email(Channel):
    def __init__(self,
                 name,
                 sender,
                 recipient,
                 smtp_address,
                 username=None,
                 password=None,
                 tls=False,
                 ssl=True,
                 port=587):
        super(Email, self).__init__()
        self.name = name
        self.recipient = recipient
        self.sender = sender
        self.email = EasySender(smtp_address=smtp_address,
                                username=username,
                                password=password,
                                ssl=ssl,
                                tls=tls,
                                port=port)

    def notify(self, **kwargs):
        result = self.email.send(sender=self.sender,
                                 recipients=self.recipient,
                                 subject=kwargs.get('subject'),
                                 body=kwargs.get('message'))
        if not result:
            self._logger.error('Failed sending email')
        return result
