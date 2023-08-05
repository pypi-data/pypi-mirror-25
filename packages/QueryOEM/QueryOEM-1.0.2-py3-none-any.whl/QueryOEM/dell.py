# -*- coding: utf-8 -*-
'''
Program: DellScrapping/Main
Dev: Fabricio Roberto Reinert
Date: 30/06/2017

Code content is intended to support Dell web scrapping

The class DellScrapper need to be up-to-date with Dell's website structure
If you're planning to update it by yourself, do it on the following methods:
    DellScrapper.warranty_to_dict()
    DellScrapper.sysconfig_to_dict()

Don't forget to <return> the result dictionary at the end of the methods!  
'''

import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
import QueryOEM.errors as errors
import QueryOEM.converters as converters
	

class DellScrapper():
    '''Dell Web scrapping'''

    def __init__(self, **settings):

        # Check information
        if not settings['warranty_url']:
            raise errors.DellScrapperFailure("Failure gathering warranty HTML content")

        if not settings['config_url']:
            raise errors.DellScrapperFailure("Failure gathering system HTML content")

        if not settings['partnumber']:
            raise errors.DellScrapperFailure("Part number not defined")

        # add configuration
        self.conf = settings
        
        # response from DELL's request 
        r_warranty, r_syconfig = self.make_requests(
            warranty_url=self.conf['warranty_url'], 
            sysconfig_url=self.conf['config_url']
        ) 

        # Check if Tag was found
        if r_warranty or r_syconfig:
            
            # Parse, process and persist data into a dictionary 
            warranty, send_date = self.warranty_to_dict(r_warranty)
            system_configuration = self.sysconfig_to_dict(r_syconfig)
            self.data = {
                'send_date': send_date,
                'warranty': warranty,
                'sysconfig': system_configuration
            }

        else:
            self.data = {
            'send_date': '',
            'warranty': '',
            'sysconfig': ''
        }

    def warranty_to_dict(self, content):
        '''Create a dictionary containing warranty data'''

        b = bs(content, 'html.parser')
        try:
            tr = b.find_all('tr')
            
            # When Dell sended the workstation
            date_send = tr[0].find_all('th')[1].text # Return raw text
            date_send = date_send.replace('Data de envio: ','').replace(',','').replace(' ','') # remove bad chars
            date_send = converters.verb_month_to_number_br(date_send) # Convert to enumerated month
            date_send = datetime.strptime(date_send, '%m%d%Y').strftime('%m/%d/%y') # format date

            # Warrantys
            all_warrantys = []
            warrantys = b.find('tbody')
            for warranty in warrantys.find_all('tr'):
                
                # Date start warranty
                start_warranty = warranty.find_all('td')[1].text
                start_warranty = start_warranty.replace('\r\n', '').replace(',','').replace(' ','').replace('\n','') # Remove bad chars
                start_warranty = converters.verb_month_to_number_br(start_warranty) # Convert to enumerated month
                start_warranty = datetime.strptime(start_warranty, '%m%d%Y').strftime('%m/%d/%y') # format date

                # Date end warranty
                end_warranty = warranty.find_all('td')[2].text
                end_warranty = converters.verb_month_to_number_br(end_warranty)
                end_warranty = end_warranty.replace(',','').replace(' ','')
                end_warranty = datetime.strptime(end_warranty, '%m%d%Y').strftime('%m/%d/%y')

                w = {
                    'plan': warranty.find_all('td')[0].text,
                    'start': start_warranty,
                    'end': end_warranty,
                }
                all_warrantys.append(w)

        except:
            raise errors.DellScrapperFailure("failed when passing warranty to dict")

        return all_warrantys, date_send

    def sysconfig_to_dict(self, content):
        '''Create a dictionary containing system configuration'''
        b = bs(content, 'html.parser')
        try:
            table = b.find_all("table", {"class":"table"})

            # Get model
            model = table[0].find_all("td")[3].string.replace('\r\n','').replace(' ','')

            # Get country
            country = table[0].find_all("td")[7].string.replace('\r\n','').replace(' ','')

            # Components
            comps = b.find_all("div", {"class":"top-offset-20"})
            components = []
            for colapsed in comps[:-1]:
                # component header
                part = colapsed.find("span", {"class": "show-collapsed"}).text.split(':')
                code = part[0][:-1]
               
                # There is no description in some cases
                if len(part) > 1:
                    description = part[1][1:]
                else:
                    description = ''

                components.append({'code':code, 'description':description})
            

        except:
            raise errors.DellScrapperFailure("failed when passing system config to dict")
            pass

        return {
            'model': model,
            'country': country,
            'components': components
        }

    def make_requests(self, warranty_url, sysconfig_url):
        '''Request data from DELL. Returning False means the TAG was not found'''

        def request_warranty(url):
            '''GET request to warranty page'''
            __url = url.format(self.conf['partnumber'])
            r = requests.get(__url)
            
            # 200 is OK
            if r.status_code != 200:
                raise errors.RequestFailed(r.status_code)
            
            # diferent url means redirected because it was not found 
            if r.url != __url:
                return False
            return r.content

        def request_system_config(url):
            '''GET request to warranty page'''
            __url = url.format(self.conf['partnumber'])
            r = requests.get(__url)

            # 200 is OK
            if r.status_code != 200:
                raise errors.RequestFailed(r.status_code)

            # diferent url means redirected because it was not found
            if r.url != __url:
                return False
            return r.content

        response_warranty = request_warranty(warranty_url)
        response_sysconfig = request_system_config(sysconfig_url)

        return response_warranty, response_sysconfig