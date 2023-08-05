# -*- coding: utf-8 -*-
'''
Program: DellScrapping/Main
Dev: Fabricio Roberto Reinert
Date: 30/06/2017

Core of this module.
Make sure you understand the the Requests lib & Beatifull Soup 4 lib

WARNING. If you're planning to use the <MultipleQueryOEM> you need to know 2 thigs:
    1. This code is not multi threaded
    2. The OEM may request a CAPTCHA after too much requests. Don't make your service tag list too big 
'''
import json
import QueryOEM.conf as conf
import QueryOEM.dell as dell
import QueryOEM.errors as errors

AVAILABLE_OEM = [
    'DELL',
]

AVAILABLE_FORMAT = [
    'JSON',
]

def check_oem(input: str) -> bool:
    if input.upper() in AVAILABLE_OEM:
        return True
    return False

def check_format(input: str) -> bool:
    if input.upper() in AVAILABLE_FORMAT:
        return True
    else:
        return False

class QueryOEM:
    '''Class responsible for the Scrapping'''

    def __init__(self, **settings):

        # Settings    
        config = conf.Settings(settings=settings)
        self.settings = config.config()

        # Initialize _dell_data
        self._dell_data = {} 

        # Check if partnumber was entered
        if not 'PART_NUMBER' in self.settings:
            raise errors.InvalidSerialList("Part number not informed")

    ### Properties ###
    @property
    def part_number(self):
        '''Will be used to check PN consistency in the future'''
        return self._part_number 

    @property
    def dell_data(self):
        '''Return a dictionary with the scrapped data'''
        return self._dell_data

    ### Setters ###
    @part_number.setter
    def part_number(self, value):
        '''Part Number SETTER''' 
        self._part_number = value

    @dell_data.setter
    def dell_data(self, value):
        self._dell_data = value
        
    ### Methods ###
    def get_from_dell(self):
        '''Issue data from Dell'''
        dell_scrapper = dell.DellScrapper(
            warranty_url=self.settings['DELL_SUPPORT_WARRANTY'],
            config_url=self.settings['DELL_SUPPORT_CONFIG'],
            partnumber=self.settings['PART_NUMBER']
        )
        pn = self.settings['PART_NUMBER']
        self.dell_data[pn] = dell_scrapper.data

    def json_from_dell(self):
        '''Return serialized data to json'''
        return json.dumps(self._dell_data)

class MultipleQueryOEM:
    '''Main class wraper to query multiple tags'''
    
    @property
    def results(self):
        '''Persist Query instances'''
        return self._results

    def __init__(self, servicetags, **settings):

        # Check if service tags were passed correctly
        if not ((isinstance(servicetags, list)) or (isinstance(servicetags, tuple))):
            raise errors.InvalidSerialList("Parameter <List> or <tuple> required")

        # Settings    
        config = conf.Settings(settings=settings)
        self.settings = config.config()

        # Initialize Results property
        self._results = []
        
        # Persist services tags
        self.part_numbers = []
        for i in servicetags:
            self.part_numbers.append(i) 

    def get_from_dell(self, verbose=True):
        '''Query all tags on Dell'''
        
        def std(txt):
            if verbose:
                print(txt)
        
        std("Start Quering the list...")
        for st in self.part_numbers:
            std("Quering {0}".format(st))
            query = QueryOEM(
                DELL_SUPPORT_WARRANTY = self.settings['DELL_SUPPORT_WARRANTY'], 
                DELL_SUPPORT_CONFIG = self.settings['DELL_SUPPORT_CONFIG'],
                PART_NUMBER = st,
            )
            query.get_from_dell()
            self._results.append(query)
    
    def json_from_dell(self):
        '''Return serialized data to json'''
        items = []
        for i in self._results:
            items.append(i.dell_data)

        return json.dumps(items)