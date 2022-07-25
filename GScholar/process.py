# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:26:11 2022

@author: m219613
"""

import pandas as pd
#from scihub.scihub import SciHub
# from scholarly import scholarly
from habanero import Crossref

# from scholarly import ProxyGenerator
# This needs to be done only once per session
# pg = ProxyGenerator()
# pg.FreeProxies()
# scholarly.use_proxy(pg)

cr = Crossref()

boston_url = 'Specific_tension_papers_edited.csv'
boston_df=pd.read_csv(boston_url)
# boston_df.sort_values(by=['Citation'], inplace=True, ascending=False, na_position='first')

new_title=[]
for title in boston_df['Paper Title']:
    search_string=title.replace('[HTML]', '')
    search_string=search_string.replace('[PDF]','')
    print(search_string)
    new_title.append(search_string)
    
    # search_query = scholarly.search_pubs(search_string)
    # scholarly.pprint(next(search_query))
    # x = cr.works(query = search_string)
    # x['message']
    # x['message']['total-results']
    # x['message']['items']    
    
boston_df['Paper Title']=new_title
boston_df.to_csv('Specific_tension_papers_edited.csv', sep=',', index=False,header=True)    
# sh = SciHub()   
# results = sh.search('Specific tension human muscle', 5)  
# sh.download(results['url'],path='papers/paper.pdf')
