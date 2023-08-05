#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: stdout.py


from notifierlib.notifierlib import Channel


__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''18-09-2017'''


class Stdout(Channel):
    """A simple library to print to stdout"""

    def __init__(self, name):
        self.name = name

    def notify(self, **kwargs):
        print('Subject :{}'.format(kwargs.get('subject')))
        print('Message :{}'.format(kwargs.get('message')))
        print()
        return True
