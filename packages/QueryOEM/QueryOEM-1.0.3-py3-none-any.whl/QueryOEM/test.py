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

import QueryOEM.scrapping as scrapping


# Test variables 
part_num_list = [] # Several service tags - MultiQueryTest()
multi_query_file = 'c:/temp/multiquerydell.json' # Target output for multiple querys
single_query_file = 'c:/temp/singlequerydell.json' # Target output for single query


def MultiQueryTest():
    '''Use the wrapper to test module'''
    try:
        # Instantiate
        obj = scrapping.MultipleQueryOEM(part_num_list)
        obj.get_from_dell()

        # Serialize JSON
        single_json = obj.results[0].json_from_dell()
        json_data = obj.json_from_dell()
    except BaseException as e:
        print(">> Error instantiating main Class: {0}".format(e))
        raise
    
    # Output JSON for Multi Query
    fopen = open(multi_query_file, 'w')
    fopen.write(json_data)
    fopen.close()

    # Output JSON for single Query
    fopen = open(single_query_file, 'w')
    fopen.write(single_json)
    fopen.close()

# Runs the test
MultiQueryTest()