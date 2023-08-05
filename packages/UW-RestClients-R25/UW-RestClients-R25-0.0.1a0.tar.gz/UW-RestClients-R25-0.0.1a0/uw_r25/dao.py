import logging
import os
import re
from os.path import abspath, dirname
from restclients_core.dao import DAO


class R25_DAO(DAO):
    def service_name(self):
        return 'r25'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]
