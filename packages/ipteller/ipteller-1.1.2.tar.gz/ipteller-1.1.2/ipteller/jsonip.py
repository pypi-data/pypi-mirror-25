#!/usr/bin/env python

from providerip import ProviderIp


class JsonIp(ProviderIp):
    def __init__(self):
        ProviderIp.__init__(self)
        self.url = 'https://jsonip.com/'

    @staticmethod
    def get_ip(uri):
        return uri["ip"]
