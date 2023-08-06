# -*- coding: utf-8 -*-
from airbridge.models.nodes import Node
from airbridge.utils.user_agents import parse


class Device(Node):

    def __init__(self, initial_data={}, user_agent=None):

        # TODO validate initial_data

        # Identity
        self.deviceUUID = None 
        self.gaid = None
        self.ifv = None
        self.ifa = None
        self.facebookAttributionID = None

        # Device specs
        self.deviceModel = None
        self.manufacturer = None
        self.osName = None
        self.osVersion = None
        self.locale = None
        self.limitAdTracking = None
        self.limitAppTracking = None
        self.timezone = None
        self.deviceIP = None
        self.clientIP = None
        self.orientation = None
        self.screen = {
            "width": "",
            "height": "", 
            "density": "" 
        }
        self.network = {
            "carrier": "", 
            "bluetooth": "", 
            "cellular": "", 
            "wifi": "",
        }
        self.location = {
            "latitude": "", 
            "longitude": "", 
            "altitude": "", 
            "speed": "" ,
        }

        for key in initial_data:
            setattr(self, key, initial_data[key])

        # 하나의 이벤트를 처리하는 것이므로
        # 복수개의 앱 혹은 브라우져를 가질 수 없다.
        self.browser = None
        self.app = None

    def get_attributes_as_dict(self):
        mock = self.__dict__.copy()
        del mock['browser']
        return mock

    def has_browser(self, browser):
        # TODO Browser 객체인지 확인
        # init with user_agent
        self.browser = browser
        if self.browser.user_agent is not None:
            self.__init_with_browser_user_agent(self.browser.user_agent)

    def __init_with_browser_user_agent(self, user_agent):
        ua_parser = parse(user_agent)

        self.manufacturer = ua_parser.device.brand
        self.deviceModel = ua_parser.device.model
        self.osName = ua_parser.os.family
        self.osVersion = ua_parser.os.version_string


