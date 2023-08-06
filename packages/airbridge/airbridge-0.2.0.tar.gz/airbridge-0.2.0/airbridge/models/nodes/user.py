# -*- coding: utf-8 -*-
from airbridge.models.nodes import Node


class User(Node):

    def __init__(self, initial_data={}):

        self.externalUserID = None
        self.externalUserEmail = None

        for key in initial_data:
            setattr(self, key, initial_data[key])

    def get_attributes_as_dict(self):
        return self.__dict__

