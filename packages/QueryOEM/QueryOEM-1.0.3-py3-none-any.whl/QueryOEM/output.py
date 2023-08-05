# -*- coding: utf-8 -*-
'''
Program: DellScrapping/Output Files
Dev: Fabricio Roberto Reinert
Date: 11/09/2017
'''
from QueryOEM import scrapping as s

cli_help_file = '''
-------------------------
QueryOEM CLI - Text file
-------------------------
Arguments
    - (Required) origin - Path to file containing service tags (1 per line)
    - (Required) output - Path to output file: Path to save output file
    - (Optional) vendor - Vendor - Default Dell
    - (Optional) format - Output format - Default JSON 
Example:
    - python -m QueryOEM.fromfile --tag origin=path/to/mytags.txt output=temp/file vendor=dell format=json
    - python -m QueryOEM.fromfile --tag origin=path/mytags.txt output=file format=json
    - python -m QueryOEM.fromfile --tag origin=path/mytags.txt output=c:/temp/result vendor=dell
    - python -m QueryOEM.fromfile --tag origin=path/mytags.txt output=result format=json
'''

cli_help_singletag = '''
--------------------------
QueryOEM CLI - Single Tag
--------------------------
Arguments
    - (Required) tag - Tag code
    - (Required) vendor - OEM name. Default is Dell
Example:
    - python -m QueryOEM.cli --tag dell XYZ0000
'''

cli_help ='''
-------------
QueryOEM CLI
-------------
CLI arguments:
    - python -m QueryOEM.cli --file : Query OEM using a a file containing tags
    - python -m QueryOEM.cli --tag : Query OEM using a single tag
'''

def dell_single_asset(tag):
    query = s.QueryOEM(PART_NUMBER=tag)
    query.get_from_dell()
    return query.dell_data

def save_json_from_dell(path, extension, assets_list) -> bool:
    '''Retrieve a JSON file containing all equipments'''
    try:
        assets_list = s.MultipleQueryOEM(assets_list)
        assets_list.get_from_dell()
        JSON = assets_list.json_from_dell()
        fopen = open(path + '.' + extension.lower(), 'w')
        fopen.write(JSON)
        fopen.close()
    except BaseException as e:
        return False
    finally:
        return True