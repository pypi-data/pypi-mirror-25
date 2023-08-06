# -*- coding: UTF-8 -*-
"""
A scraper utility package
"""

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2014-17, Florian JUNG"
__license__ = "MIT"
__version__ = "0.2.0"
__date__ = "2017-10-12"

from .webscraper import WebScraper, default_user_agents, \
    WEBConnectException, WEBFileException, WEBParameterException
import cache
from .cache import Cache
from .models import Response, CacheInfo

__all__ = [
    "webscraper", "cache", "WebScraper", "Cache", "Response", "CacheInfo"
]
