# -*- coding: utf-8 -*-
from airbridge.models.nodes import Node


class MobileApp(Node):

    def __init__(self, initial_data={}):

        self.appID = None
        self.version = None
        self.versionCode = None
        self.packageName = None

        for key in initial_data:
            setattr(self, key, initial_data[key])

    def get_attributes_as_dict(self):
        return self.__dict__

    def triggers_event(self, event_data):
        # event node
        return event_data
