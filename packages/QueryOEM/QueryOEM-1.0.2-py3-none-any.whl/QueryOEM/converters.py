# -*- coding: utf-8 -*-
'''
Program: DellScrapping/Main
Dev: Fabricio Roberto Reinert
Date: 30/06/2017

Converters for HTML Parsers

Use this file if you need to convert any data type from HTML
This method intend to keep the core code cleaner
'''

def verb_month_to_number_br(month):
    '''enumerate verbose month'''
    m = month
    if 'janeiro' in m:
        m = m.replace('janeiro','01')

    if 'fevereiro' in m:
        m = m.replace('fevereiro','02')

    if 'março' in m:
        m = m.replace('março','03')

    if 'abril' in m:
        m = m.replace('abril','04')

    if 'maio' in m:
        m = m.replace('maio','05')

    if 'junho' in m:
        m = m.replace('junho','06')

    if 'julho' in m:
        m = m.replace('julho','07')

    if 'agosto' in m:
        m = m.replace('agosto','08')

    if 'setembro' in m:
        m = m.replace('setembro','09')

    if 'outubro' in m:
        m = m.replace('outubro','10')

    if 'novembro' in m:
        m = m.replace('novembro','11')

    if 'dezembro' in m:
        m = m.replace('dezembro','12')
        
    return m