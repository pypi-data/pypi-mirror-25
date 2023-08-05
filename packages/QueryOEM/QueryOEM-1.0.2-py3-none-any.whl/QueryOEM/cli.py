# -*- coding: utf-8 -*-
'''
Program: Scrapping/Output CLI
Dev: Fabricio Roberto Reinert
Date: 11/09/2017
'''
from sys import argv
from os import path
from pathlib import Path
from QueryOEM.scrapping import check_format, check_oem
import QueryOEM.output as out

def service_tag_from_file(origin):
    '''reads the file containing tags and return a list'''
    __tags = []
    __fopen = open(origin, 'r')
    for i in __fopen:
        __tags.append(i.rstrip())
    return __tags

def query_oem(*args):
    '''CLI. Query a single tag'''
    leng = len(args)
    arguments = {}

    if leng != 3:
        print('>> There are required parameters missing')
        print(out.cli_help_singletag)
        return

    arguments['vendor'] = args[1]
    arguments['tag'] = args[2]

    # Query Dell
    if arguments['vendor'].upper() == 'DELL':
        return out.dell_single_asset(arguments['tag'])
    else:
        print('>> Invalid arguments')
        print(out.cli_help_singletag)
        return

def query_from_file(*args):
    '''CLI - Query OEM using a TAG file"'''
    
    arguments = {}
    leng = len(args)

    # Check if required args are passed
    if leng < 3:
        print('>> There are required parameters missing')
        print(out.cli_help_file)
        return

    elif len(args) > 2:
        for arg in args[1:]:
            try:
                split_arg = arg.split('=')
                arguments[split_arg[0]] = split_arg[1]
            except:
                print('>>Malformed parameters')
                print(out.cli_help_file)
                return
    
    # Check if we got the required params
    if 'origin' not in arguments.keys():
        print('>> Parameter ORIGIN not informed')
        print(out.cli_help_file)
        return

    if 'output' not in arguments.keys():
        print('>> Parameter OUTPUT not informed')
        print(out.cli_help_file)
        return

    if 'vendor' not in arguments.keys():
        arguments['vendor'] = 'DELL'

    if 'format' not in arguments.keys():
        arguments['format'] = 'JSON'

    # Check if tag file is valid
    if not Path(arguments['origin']).is_file():
        print('>> File containing tags is invalid')
        print(out.cli_help_file)
        return

    # Check if target folder is valid
    out_path, out_file = path.split(arguments['output']) 
    if not Path(out_path).is_dir():
        print('>> Output path is invalid')
        print(out.cli_help_file)
        return

    # check if OEM typed is available
    if not check_oem(arguments['vendor']):
        print('>> This vendor is not available')
        print(out.cli_help_file)
        return

    # check if format is valid
    if not check_format(arguments['format']):
        print('>> File format not supported')
        print(out.cli_help_file)
        return

    # Get Tags from file
    tag_list = service_tag_from_file(arguments['origin'])
    
    # Save JSON file from Dell
    if arguments['format'].upper() == 'JSON' and arguments['vendor'].upper() == 'DELL': 
        if not out.save_json_from_dell(arguments['output'], arguments['format'], tag_list):
            return '>> Process with errors'
        else:
            return '>> Process completed'

if __name__ == '__main__':

    # No arguments provided
    if len(argv) == 1:
        print(out.cli_help)
        quit()

    # Query from text file
    if argv[1] == '--file':
        print('>> Requesting data from OEM...')
        result = query_from_file(*argv[1:])
        print(result)

    # Single Tag
    elif argv[1] == '--tag':
        print('>> Requesting data from OEM...')
        result = query_oem(*argv[1:])
        print(result)
    
    # Wrong primary argument
    else:
        print(out.cli_help)
        quit()