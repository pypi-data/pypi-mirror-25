# -*- coding: utf-8 -*-
from airbridge.models.nodes import Node


class Browser(Node):

    def __init__(self, user_agent='', headers={}):

        self.user_agent = user_agent 
        self.headers = {
            'user-agent': user_agent
        }
        self.headers.update(headers)

