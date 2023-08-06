# -*- coding: utf-8 -*-
import os
from airbridge import engine_configs
from sqlalchemy import create_engine
from sqlalchemy.sql import text


class BaseConfig():

    def __init__(self):
        # Engines
        READ_DB = 'mysql://{}:{}@{}/udl?charset=utf8mb4'.format(engine_configs['read_db_host'],
                                                                engine_configs['read_db_pw'],
                                                                engine_configs['read_db'],)

        MAIN_DB = 'mysql://{}:{}@{}/udl?charset=utf8mb4'.format(engine_configs['main_db_host'],
                                                                engine_configs['main_db_pw'],
                                                                engine_configs['main_db'],)

        LOG_DB = 'mysql://{}:{}@{}/udl?charset=utf8mb4'.format(engine_configs['log_db_host'],
                                                               engine_configs['log_db_pw'],
                                                               engine_configs['log_db'],)
        self.engine = create_engine(MAIN_DB, convert_unicode=True)
        self.read_engine = create_engine(READ_DB, convert_unicode=True)
        self.log_engine = create_engine(LOG_DB, convert_unicode=True)

        # Hosts
        self.host = engine_configs['dev_abrge']
        self.short_host = engine_configs['dev_abrge']
        self.core_host = engine_configs['dev_core_airbridge']
        self.sdk_host = engine_configs['dev_sdk_airbridge']
        self.test_host = engine_configs['dev_test_airbridge']
        self.ads_host = engine_configs['dev_ads_airbridge']

        # Testing variables 
        self.headers = {'Authorization': engine_configs['jwt_token'], 'Content-Type': 'application/json'}

    def change_localhost_port(self, port):
        self.host = self.host.replace('5000', str(port))
        self.core_host = self.core_host.replace('5000', str(port))


