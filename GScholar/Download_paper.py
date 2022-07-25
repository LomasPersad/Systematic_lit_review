# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:35:22 2022

@author: m219613
"""
import webbrowser
import pandas as pd


#select the url you want to open
url = 'http://docs.python.org/'

edited_file = 'Specific_tension_papers.csv'
papers_df=pd.read_csv(edited_file)

#set browser path
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

#open browser, search URL
for i in range(0,len(papers_df)) :
    if papers_df['Downloaded'][i]== True:
        print ('Already downloaded!')
        continue
    else:
        url=papers_df['Url of paper'][i]
        print(url)
#         webbrowser.get(chrome_path).open(url)