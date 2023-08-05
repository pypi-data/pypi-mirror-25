# -*- coding: utf-8 -*-
'''
Program: DellScrapping/Exceptions
Dev: Fabricio Roberto Reinert
Date: 30/06/2017
'''

class SettingsConsistency(Exception):
    '''Raise exceptions for module Settings'''

    def __init__(self, field):
        super(SettingsConsistency, self).__init__(self, "Variable {0} is not properly configured".format(field))

class InvalidSerialList(Exception):
    '''Raise exceptions for Serial List '''
    
    def __init__(self, text):
        super(InvalidSerialList, self).__init__(self, "Part Number error: {0}".format(text))

class RequestFailed(Exception):
    '''Raise exeptions for request errors'''

    def __init__(self, error_code):
        
        if error_code == 500:
            super(RequestFailed, self).__init__(self,"500 - Internal Server Error")

        if error_code == 404:
            super(RequestFailed, self).__init__(self,"404 - Page not Found")

        else:
            super(RequestFailed, self).__init__(self,"Unkown error during the request: {0}".format(str(error_code)))

class DellScrapperFailure(Exception):
    '''Raise exceptions during dell procedure'''

    def __init__(self, text):
        super(DellScrapperFailure, self).__init__(self, 'Failure while scrapping DELL: {0}'.format(text))

class CheckSettings:
    '''Check settings consistency'''

    def __init__(self, **settings):
        try:
            from conf import default_settings as settings
            import errors
        except ImportError:
            raise

        # Check Settings Consistency
        if not settings['DELL_SUPPORT_WARRANTY']:
            if not hasattr(settings, 'DELL_SUPPORT_WARRANTY'):
                raise SettingsConsistency("DELL_SUPPORT_WARRANTY")
        else:
            print('User difined DELL_SUPPORT_WARRANTY as "{0}"'.format(settings['DELL_SUPPORT_WARRANTY']))
        
        if not settings['DELL_SUPPORT_CONFIG']:
            if not hasattr(settings, 'DELL_SUPPORT_CONFIG'):
                raise SettingsConsistency("DELL_SUPPORT_CONFIG")
        else:
            print('User difined DELL_SUPPORT_CONFIG as "{0}"'.format(settings['DELL_SUPPORT_CONFIG']))