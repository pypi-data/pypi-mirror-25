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
    arguments = {'tags': []}

    # Populate arguments
    for argument in args[1:]:
        split_arg = argument.split('=')
        if len(split_arg) == 1:
            arguments['tags'].append(argument)
        elif len(split_arg) == 2:
            arguments[split_arg[0].upper()] = split_arg[1]
        else:
            print('>> Invalid parameter: %s' % argument)
            print(out.cli_help_singletag)
            return

    # Check if Tags was supplied
    if len(arguments['tags']) < 1:
        print('>> No service tag was supplied')
        print(out.cli_help_singletag)
        return

    # Check Output parameter
    if not 'OUTPUT' in arguments.keys():
        print('>> Output parameter is required')
        print(out.cli_help_singletag)
        return
    
    out_path, out_file = path.split(arguments['OUTPUT']) 
    if not Path(out_path).is_dir():
        print('>> Output path is invalid')
        print(out.cli_help_file)
        return

    # Check format parameter
    if not 'FORMAT' in arguments.keys():
        arguments['FORMAT'] = 'JSON'
    else:
        arguments['FORMAT'] = arguments['FORMAT'].upper()

    if not check_format(arguments['FORMAT']):
        print('>> Format %s not available' % arguments['FORMAT'])
        print(out.cli_help_singletag)
        return

    # Check Vender parameter
    if not 'VENDOR' in arguments.keys():
        arguments['VENDOR'] = 'DELL'
    else:
        arguments['VENDOR'] = arguments['VENDOR'].upper()
    
    if not check_oem(arguments['VENDOR']):
        print('>> Vendor %s not available' % arguments['VENDOR'])
        print(out.cli_help_singletag)
        return

    # Query Dell
    if arguments['VENDOR'] == 'DELL' and arguments['FORMAT'] == 'JSON':
        print('>> Query list: %s' % arguments['tags']) 
        if out.save_json_from_dell(arguments['OUTPUT'], arguments['tags']):
            return '>> Process completed'
        else:
            return '>> Process with errors'
    

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
        if out.save_json_from_dell(arguments['output'], tag_list):
            return '>> Process completed'
        else:
            return '>> Process with errors'

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

    # Query from terminal
    elif argv[1] == '--tag':
        print('>> Requesting data from OEM...')
        result = query_oem(*argv[1:])
        print(result)
    
    # Wrong primary argument
    else:
        print(out.cli_help)
        quit()