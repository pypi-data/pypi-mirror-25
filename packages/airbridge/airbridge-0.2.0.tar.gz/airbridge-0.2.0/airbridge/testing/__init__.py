# -*- coding: utf-8 -*-
from airbridge.testing.config import BaseConfig
from sqlalchemy.sql import text
from airbridge.utils.tools import get_md5_hash
from airbridge.models.nodes.user import User
from airbridge.models.nodes.device import Device
from airbridge.models.nodes.browser import Browser
from airbridge.models.nodes.mobile_app import MobileApp
from uuid import uuid4
from enum import Enum
import time
import unittest
import requests
import sys
from datetime import datetime
if sys.version_info[0] == 2:
    from urllib import urlencode, quote, unquote
    from urlparse import urlparse, parse_qs, urlunparse 
else:
    from urllib.parse import urlparse, parse_qs, urlunparse, quote, unquote, urlencode


class TouchTarget(Enum):
    # ADS / CLICK / GOOGLE PLATFORM MATCHING
    ADWORDS = 1
    # ADS / CLICK / FACEBOOK PLATFORM MATCHING
    FACEBOOK_BUSINESS = 2
    # NONADS / CLICK / FACEBOOK PLATFORM MATCHING
    FACEBOOK = 3

    # NONADS / CLICK, VIEW / FINGER PRINT MATCHING, REFERRER MATCHING for Android 
    WEBPAGE = 4
    # ADS  / CLICK / FINGER PRINT MATCHING, REFERRER MATCHING for Android 
    STDADS_WOID = 5
    # NONADS / CLICK / FINGER PRINT MATCHING, REFERRER MATCHING for Android 
    SIMPLELINK = 6
    # ADS / VIEW / FINGER PRINT MATCHING
    STDADS_WOID_VIEW = 7

    # ADS / CLICK / ID MATCHING, REFERRER MATCHING for Android 
    STDADS_WID = 8
    # ADS / VIEW / ID MATCHING
    STDADS_WID_VIEW = 9

    # GET FIXED SHORT ID
    APP_MARKET = 10
    UNATTRIBUTED = 11

    DEEPLINK = 12



def get_rand_hex_str():
    return uuid4().hex


def is_empty(text):
    emp_str = lambda s: s or ""

    if emp_str(text) == "":
        return True
    else:
        return False


def get_rand_str():
    return str(uuid4())


def get_query_string_part_as_dict(qs_part):
    dict_qs = parse_qs(qs_part)
    return {k: v[0] for k, v in dict_qs.items()}


def get_url_with_additional_params(url, query):
    if query is None:
        return url

    if type(url) is unicode:
        url = str(url)

    params = urlencode(query)
    url_parts = []
    url_parts = list(urlparse(url))
    url_parts[4] = urlencode(parse_qsl(url_parts[4]) + parse_qsl(params))

    return urlunparse(url_parts)


def get_datetime_from_ms(ms):
    if ms is None:
        return None

    if len(str(ms)) == 16:
        # microseconds
        return datetime.fromtimestamp(int(ms)/1000000.0)
    elif len(str(ms)) == 13:
        # milliseconds
        return datetime.fromtimestamp(int(ms)/1000.0)
    else:
        # seconds
        return datetime.fromtimestamp(int(ms))



class AirbridgeBaseTest(unittest.TestCase, BaseConfig):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        BaseConfig.__init__(self)
        self.resource = '/'

    def setUp(self):
        print(self.id() + '...............[testing]')

    def tearDown(self):
        print(self.id() + '...............[end]')

    def get_url(self):
        return self.core_host + self.resource

    @staticmethod
    def get_timestamp_day_before(day_before):
        DAY = 86400 # seconds
        return int(round(time.time() - day_before * DAY) * 1000)

    @staticmethod
    def get_timestamp_time_before(time_before):
        return int(round(time.time() - time_before) * 1000)

    def send_request(self, url, method='get', headers=None, data=None, cookies=None, allow_redirects=True):
        if headers == None:
            headers = self.headers 

        method = method.lower()

        if method == 'get':
            res = requests.get(url, headers=headers, cookies=cookies, allow_redirects=allow_redirects)
        elif method == 'post':
            res = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == 'put':
            res = requests.put(url, data=data, headers=headers, cookies=cookies)
        elif method == 'delete':
            res = requests.delete(url, data=data, headers=headers, cookies=cookies)
        else:
            print 'Now allowed method'

        return res

    def check_api_response(self, res, expected=200):
        err_msg = """Expected {0}. But we got wrong status code: {1}\nError message:\n{2}""".format(str(expected), str(res.status_code), res.text.encode('utf-8'))
        self.assertEqual(res.status_code, expected, err_msg)

        if res.status_code == expected:
            print """Test was successful. Response text below:\n{0}""".format(res.text.encode('utf-8'))

    def reset_hashstring(self, remote_addr, os_version, device_type, app_id):
        source_str = "{0}-{1}-{2}-{3}".format(remote_addr,
                                              os_version,
                                              device_type,
                                              app_id)
        hashstring = get_md5_hash(source_str)
        query_str = """
        DELETE 
        FROM tbl_installcheck
        WHERE hashstring=:hashstring
        """
        self.engine.execute(text(query_str), hashstring=hashstring)



class MobileEventSender(BaseConfig):

    def __init__(self, user=None, device=None, mobile_app=None):
        if type(user) is User:
            self.user = user
        else:
            self.user = User({
                "externalUserID": get_rand_str(),
                "externalUserEmail": get_rand_str()
            })

        if type(device) is Device:
            self.device = device
        else:
            gaid = get_rand_str() 
            self.device = Device({
                "deviceUUID": gaid,
                "gaid": gaid,
                "ifv": "",
                "ifa": "",
                "locale": 'ko-KR',
                "orientation": "portrait",
                "location": {
                    "latitude": 120.103,
                    "longitude": 120.1023412,
                    "altitude": 123.00,
                    "speed": 12
                },
                "network": {
                        "wifi": True,
                        "cellular": False,
                        "bluetooth": False,
                        "carrier": "KT",
                },
                "screen": {
                    "width": 123,
                    "height": "123",
                    "density": 2
                },
                "limitAdTracking": True,
                "limitAppTracking": 0,
                "timezone": "seoul",
                "clientIP": "127.0.0.1",
                "deviceIP": "127.0.0.1"
            })
            user_agent = 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Mobile Safari/537.36'
            self.device.has_browser(Browser(user_agent=user_agent))

        if type(mobile_app) is MobileApp:
            self.mobile_app = mobile_app
        else:
            self.mobile_app = MobileApp({
                                "appID": 619,
                                "version": "1.2.3",
                                "versionCode": "4.5",
                                "packageName": "com.ab180.co",
                              })

        self.app_id = self.mobile_app.appID
        self.sdk_version = "T_A_v2.0"

        print self.device.deviceUUID

    def get_mobile_event_fomatted_data(self, event):
        return {
            "user": self.user.get_attributes_as_dict(),
            "device": self.device.get_attributes_as_dict(),
            "app": self.mobile_app.get_attributes_as_dict(),
            "eventData": event,
            "eventTimestamp": int(time.time()*(10**3)),   
            "requestTimestamp": int(time.time()*(10**3)),   
            "sdkVersion": self.sdk_version,
        }

    def get_event_data(self, deeplink=None, googleReferrer=None, exActiveStatus=1, page__label=None, page__name=None, page__customAttributes={}, goal__category=None, goal__action=None, goal__label=None, goal__value=None, goal__customAttributes={}, adwordsPostback=None, facebook_short_id=None, semantic_attributes={}, event_category=None):
        data = { 
            "eventCategory": event_category,
            "exActiveStatus": exActiveStatus,
            "googleReferrer": googleReferrer,
            "deeplink": deeplink,
            "goal": {       
                "category": goal__category, 
                "action": goal__action, 
                "label": goal__label, 
                "value": goal__value, 
                "semanticAttributes": semantic_attributes,
                "customAttributes": goal__customAttributes,
            },
            "page": {   
                "label": page__label, 
                "name": page__name,  
                "customAttributes": page__customAttributes,
            },

            # 이것이 있으면 테스트로 빠짐
            'adwordsPostback': adwordsPostback
        }

        if facebook_short_id is not None:
          data.update({
              "facebookPostbackResult": {
                  "applink_url": "ablog://?airbridge=true&airbridge_sid={0}".format(facebook_short_id),
                  "applink_args": {
                      "version":2, 
                      "bridge_args": {
                          "method": "applink"
                      },
                      "method_args": {
                          "target_url": "http://abr.ge/{}".format(facebook_short_id)
                      },
                  },
              }
          })

        return data



class UserTouchPoint(BaseConfig):

    def __init__(self, *args, **kwargs): 
        
        BaseConfig.__init__(self)

        self.resource_uri = None
        self.postback = None
        self.referrer = None
        self.cookies = args[3] if len(args) > 3 else None
        self.device = args[0] # device
        self.timestamp = args[2]
        self.ad_channel = kwargs.get('ad_channel') or 'ab180ads'

        self.setTarget(args[1])

    def set_cookie(self, cookie):
        self.cookies = cookie

    def getTarget(self):
        return self.__target

    def setTarget(self, target):
        self.__target = target

        click_id = get_rand_hex_str()
        campaign = get_rand_hex_str()
        ad_group = get_rand_hex_str()
        ad_creative = get_rand_hex_str()
        gclid = get_rand_hex_str()

        if target == TouchTarget.ADWORDS:
            # 구글 광고를 클릭 (postback 조정)
            self.resource_uri = get_url_with_additional_params(self.ads_host + '/ablog/adwords/tracking', {
                'lpurl': quote('https://play.google.com/store/apps/details?id=product.dp.io.ab180blog'),
                'campaignid': campaign,
                'adgroupid': ad_group,
                'feeditemid': '',
                'targetid': '',
                'loc_interest_ms': '',
                'loc_physical_ms': '',
                'matchtype': '',
                'network': 'd',
                'device': 'm',
                'devicemodel': 'samsung%2Bsm-g720n0',
                'creative': ad_creative,
                'keyword': '',
                'placement': 'zzzscore.com',
                'target': 'mobileappcategory%3A%3A60004',
                'adposition': 'none',
                'gclid': gclid,
                'abmacro_dynamic_timestamp': self.timestamp
            })
            self.postback = self.ads_host + "/ablog/adwords/postback?md5_advertising_id={md5_advertising_id}&adid={adid}&lat={lat}&click_url={click_url}&click_ts={click_ts}&campaign_id={campaign_id}&video_id={video_id}".format(md5_advertising_id=self.device.deviceUUID, adid=self.device.deviceUUID, campaign_id=campaign, lat=0, click_url=quote(self.resource_uri), video_id=None, click_ts=self.timestamp)
        elif target == TouchTarget.WEBPAGE:
            # 웹페이지에서 앱 설치를 클릭
            self.resource_uri = self.sdk_host + '/api/v1/apps/ablog/stats'
        elif target == TouchTarget.DEEPLINK:
            self.resource_uri = self.sdk_host + '/api/v1/apps/ablog/stats'
        elif target == TouchTarget.STDADS_WID:
            # 광고매체에서 표준광고 tracking template 호출 (with ID)
            self.resource_uri = self.ads_host + '/ablog/{ad_channel}/tracking/s?click_id={click_id}&campaign_id={campaign}&ad_group={ad_group}&ad_creative={ad_creative}&ad_id={ad_id}&abmacro_dynamic_timestamp={timestamp}&source=airbridge_param_test'.format(ad_channel=self.ad_channel, click_id=click_id, campaign=campaign, ad_group=ad_group, ad_creative=ad_creative, ad_id=self.device.deviceUUID, timestamp=self.timestamp)
        elif target == TouchTarget.STDADS_WID_VIEW:
            # 광고매체에서 표준광고 tracking template 호출 (with ID & 조회형 광고)
            self.resource_uri = self.ads_host + '/ablog/{ad_channel}/tracking/s?ad_type=view&click_id={click_id}&campaign_id={campaign}&ad_group={ad_group}&ad_creative={ad_creative}&ad_id={ad_id}&abmacro_dynamic_timestamp={timestamp}'.format(ad_channel=self.ad_channel, click_id=click_id, campaign=campaign, ad_group=ad_group, ad_creative=ad_creative, ad_id=self.device.deviceUUID, timestamp=self.timestamp)
        elif target == TouchTarget.STDADS_WOID:
            # 광고매체에서 표준광고 tracking template 호출 (without ID)
            self.resource_uri = self.ads_host + '/ablog/{ad_channel}/tracking/s?click_id={click_id}&campaign_id={campaign}&ad_group={ad_group}&ad_creative={ad_creative}&abmacro_dynamic_timestamp={timestamp}'.format(ad_channel=self.ad_channel, click_id=click_id, campaign=campaign, ad_group=ad_group, ad_creative=ad_creative, timestamp=self.timestamp)
        elif target == TouchTarget.STDADS_WOID_VIEW:
            # 광고매체에서 표준광고 tracking template 호출 (without ID & 조회형 광고)
            self.resource_uri = self.ads_host + '/ablog/{ad_channel}/tracking/s?ad_type=view&click_id={click_id}&campaign_id={campaign}&ad_group={ad_group}&ad_creative={ad_creative}&abmacro_dynamic_timestamp={timestamp}'.format(ad_channel=self.ad_channel, click_id=click_id, campaign=campaign, ad_group=ad_group, ad_creative=ad_creative, timestamp=self.timestamp)
        elif target == TouchTarget.SIMPLELINK:
            # 심플링크 클릭
            self.resource_uri = self.short_host + '/@ablog/attribution_test_channel?campaign={campaign}&ad_group={ad_group}&ad_creative={ad_creative}&abmacro_dynamic_timestamp={timestamp}'.format(click_id=click_id, campaign=campaign, ad_group=ad_group, ad_creative=ad_creative, timestamp=self.timestamp)
        elif target == TouchTarget.FACEBOOK_BUSINESS:
            pass
        elif target == TouchTarget.FACEBOOK:
            pass
        elif target == TouchTarget.APP_MARKET:
            pass
        elif target == TouchTarget.UNATTRIBUTED:
            pass
        else:
            raise Exception("Wrong target")

    target = property(getTarget, setTarget)

    def send_request(self, url, method='get', headers=None, data=None, allow_redirects=False, cookies=None):
        url = url.replace('http://abr.ge', self.host)
        url = url.replace('http://ads.airbridge.io', self.ads_host)

        if headers is None and self.device.browser is not None:
            headers = self.device.browser.headers

        if cookies is None:
            cookies = self.cookies

        if method == 'get':
            res = requests.get(url, headers=headers, allow_redirects=allow_redirects, cookies=cookies)
        elif method == 'post':
            res = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == 'put':
            res = requests.put(url, data=data, headers=headers, cookies=cookies)
        elif method == 'delete':
            res = requests.delete(url, headers=headers, cookies=cookies)
        else:
            print 'Now allowed method'

        return res

    def send_event(self, predefined_cookies=None):

        res = None
        self.cookies = predefined_cookies if predefined_cookies != None else self.cookies

        if self.__target == TouchTarget.ADWORDS:
            # 구글 광고를 클릭 (postback 조정)
            res = self.send_request(self.resource_uri, 'get', allow_redirects=False)
            try:
                if self.device.osName.lower() == 'android':
                    self.short_id = unquote(res.text).split('short_id=')[1].split('&')[0]
                    self.referrer = unquote(res.text).split('referrer=')[1].split('"')[0]
                else:
                    self.short_id = res.text.split('airbridge_sid=')[1].split('"')[0]
            except IndexError:
                raise Exception("Cannot get short_id")

        elif self.__target == TouchTarget.WEBPAGE:
            cid = self.cookies.get('ab180ClientId') if self.cookies is not None else None
            res_body = self.send_websdk_stats_event(self.resource_uri, 9224, cid=cid)
            self.short_id = res_body['simpleLink'].split('/')[-1]

        elif self.__target == TouchTarget.DEEPLINK:
            cid = self.cookies.get('ab180ClientId') if self.cookies is not None else None
            res_body = self.send_websdk_stats_event(self.resource_uri, 9226, target_url="ablog://product/123", cid=cid)
            self.deeplink = res_body['targetUrl']
            self.short_id = res_body['simpleLink'].split('/')[-1]

        elif self.__target == TouchTarget.STDADS_WID_VIEW:
            res = self.send_request(self.resource_uri, 'get', allow_redirects=False)
            res_t = eval(res.text)
            self.short_id = res_t['simplelink'].split('/')[-1]

        elif self.__target == TouchTarget.STDADS_WID:
            res = self.send_request(self.resource_uri, 'get', allow_redirects=False)
            try:
                if self.device.osName.lower() == 'android':
                    self.short_id = unquote(res.text).split('short_id=')[1].split('&')[0]
                    self.referrer = unquote(res.text).split('referrer=')[1].split('"')[0]
                else:
                    self.short_id = res.text.split('airbridge_sid=')[1].split('"')[0]
            except IndexError:
                raise Exception("Cannot get short_id")

        elif self.__target == TouchTarget.STDADS_WOID:
            res = self.send_request(self.resource_uri, 'get', allow_redirects=False)
            try:
                if self.device.osName.lower() == 'android':
                    self.short_id = unquote(res.text).split('short_id=')[1].split('&')[0]
                    self.referrer = unquote(res.text).split('referrer=')[1].split('"')[0]
                else:
                    self.short_id = res.text.split('airbridge_sid=')[1].split('"')[0]
            except IndexError:
                raise Exception("Cannot get short_id")

        elif self.__target == TouchTarget.SIMPLELINK:
            if self.device.osName.lower() == 'android':
                try:
                    # chrome
                    res = self.send_request(self.resource_uri, 'get', allow_redirects=True)
                    res = res.history[-1]
                    self.short_id = unquote(res.text).split('short_id=')[1].split('&')[0]
                    self.referrer = unquote(res.text).split('referrer=')[1].split('"')[0]
                except requests.exceptions.InvalidSchema as e:
                    # Not chrome 
                    self.short_id = str(e).split('airbridge_sid%3D')[1].split("'")[0]
                    self.referrer = str(e).split('referrer=')[1].split("'")[0]
            else:
                try:
                    res = self.send_request(self.resource_uri, 'get', allow_redirects=True)
                except requests.exceptions.InvalidSchema as e:
                    self.short_id = str(e).split('airbridge_sid=')[1].split("'")[0]

        elif self.__target == TouchTarget.FACEBOOK_BUSINESS:
            self.short_id = 'gbnh'

        elif self.__target == TouchTarget.FACEBOOK:
            self.short_id = 'oqbj'

        elif self.__target == TouchTarget.APP_MARKET:
            self.short_id = 'sleq'
            self.referrer = 'utm_source=google-play&utm_medium=app-market'

        elif self.__target == TouchTarget.UNATTRIBUTED:
            self.short_id = 'evk1'

        self.cookies = res.cookies if res != None else self.cookies
        return self.cookies

    def send_websdk_stats_event(self, resource_url, event_category, short_id=None, target_url='http://airbridge.io', cid=None, tid=None):
        self.sample_data = json.dumps({
            'airbridgeCid': get_rand_str() if cid is None else cid,
            'airbridgeTid': get_rand_str() if tid is None else tid,
            'eventCategory': event_category, # web site view event category
            'targetUrl': target_url,
            'sdkVersion': 'W_SDK_vTEST',
            'airbridgeSid': short_id,
            "simplelinkData": {
                'channel': 'attribution_test_channel',
                'params': {
                    'campaign': get_rand_hex_str(),
                    'abmacro_dynamic_timestamp': str(self.timestamp)
                }
            }
        })
        res = self.send_request(resource_url, data=self.sample_data, method='post')
        self.assert_response_status_code(res) # expect to be 200
        return json.loads(res.text)

    def assert_response_status_code(self, res, expected=200):
        err_msg = """Expected {0}. But we got wrong status code: {1}\nError message:\n{2}""".format(str(expected), str(res.status_code), res.text.encode('utf-8'))

        if res.status_code == expected:
            print """Test was successful. Response text below:\n{0}""".format(res.text.encode('utf-8'))


def send_touchpoint_events(touch_points):

    prev_cookies = None

    for tp in touch_points:
        prev_cookies = tp.send_event(predefined_cookies=prev_cookies)
        print "short_id: {0} on {1}".format(tp.short_id, get_datetime_from_ms(tp.timestamp))


# 사용자 Device
class UserDevice():

    def __init__(self, platform, device_uuid=None, ua_string=None):

        self.deviceUUID = get_rand_str() if device_uuid is None else device_uuid
        self.osName = platform.lower()
        self.browser = Browser()

        if self.osName.lower() == 'ios':
            self.browser.headers = self.set_to_ios_device()
        else:
            self.browser.headers = self.set_to_android_chrome()

        if ua_string is not None:
            self.browser.headers = {'user-agent': ua_string}

    def set_to_android_default_browser(self):
        # android chrome
        self.browser.headers = {'user-agent': DEVICE_OS_BROWSER_UA['mobile__android__default_browser']}
        return self.browser.headers

    def set_to_android_chrome(self):
        # android chrome
        self.browser.headers = {'user-agent': DEVICE_OS_BROWSER_UA['mobile__android__chrome']}
        return self.browser.headers

    def set_to_ios_device(self):
        # iphone 9
        self.browser.headers = {'user-agent': DEVICE_OS_BROWSER_UA['mobile__ios__safari']}
        return self.browser.headers

    def set_to_desktop_device(self):
        # window 7
        self.browser.headers = {'user-agent': DEVICE_OS_BROWSER_UA['desktop__window__chrome']}
        return self.browser.headers

    def set_to_ipad_device(self):
        # ipad 9
        self.browser.headers = {'user-agent': DEVICE_OS_BROWSER_UA['tablet__ios__safari']}
        return self.browser.headers


