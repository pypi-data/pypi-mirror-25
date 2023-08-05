# -*- coding: utf-8 -*-
"""
Program: DellScrapping/Settings
Dev: Fabricio Roberto Reinert
Date: 30/06/2017

Conf is a submodule to deal with settings at user level
user will be able to specify a dictionary 
or the module will load default values 
"""

# DELL URIs 
DELL_SUPPORT_WARRANTY = "http://www.dell.com/support/home/br/pt/brdhs1/product-support/servicetag/{0}/warranty"
DELL_SUPPORT_CONFIG = "http://www.dell.com/support/home/br/pt/brdhs1/product-support/servicetag/{0}/configuration"

class Settings:
    '''Retrieve a dict of settings'''

    def __init__(self, **settings):

        self.conf = {}

        # Dell variables
        if not 'DELL_SUPPORT_WARRANTY' in settings['settings']:
            global DELL_SUPPORT_WARRANTY
            self.conf['DELL_SUPPORT_WARRANTY'] = DELL_SUPPORT_WARRANTY
        else:
             self.conf['DELL_SUPPORT_WARRANTY'] = settings['settings']['DELL_SUPPORT_WARRANTY']
        
        if not 'DELL_SUPPORT_CONFIG' in settings['settings']:
            global DELL_SUPPORT_CONFIG
            self.conf['DELL_SUPPORT_CONFIG'] = DELL_SUPPORT_CONFIG
        else:
            self.conf['DELL_SUPPORT_CONFIG'] = settings['settings']['DELL_SUPPORT_CONFIG']

        # Part number variable
        if 'PART_NUMBER' in settings['settings']:
            self.conf['PART_NUMBER'] = settings['settings']['PART_NUMBER']

    def config(self):
        return self.conf