# -*- coding: utf-8 -*-
'''
Program: DellScrapping/TestUnit
Dev: Fabricio Roberto Reinert
Date: 30/06/2017

WARNING. It's necessary to fill <part_num_list>

Test environment.
This code is used to check the module consistency.
As soon as DELL or other future supported OEM change their website
this module may stop working. It's imperative to test this module periodcaly 
'''

from sys import argv
import QueryOEM.scrapping as scrapping
import QueryOEM.cli as cli
import unittest


class MultuQueryTest(unittest.TestCase):
    '''Test class for Web Scrapping objects'''
    part_num_list = [x for x in argv[1:]] # Several service tags - MultiQueryTest() - Pass as argument
    multi_query_file = 'multiquery_dell.json' # Target output for multiple querys
    single_query_file = 'singlequery_dell.json' # Target output for single query

    def MultiQueryTest():
        '''Use the wrapper to test module'''
        pass

    def ModuleCliTest():
        '''Test the CLI commands'''
        pass