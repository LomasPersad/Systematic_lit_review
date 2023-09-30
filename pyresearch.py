# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:45:09 2022

@author: m219613

"""
#Location of package
# C:\Users\m219613\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\pyResearchInsights

from pyResearchInsights.common_functions import pre_processing
from pyResearchInsights.Scraper import scraper_main
from pyResearchInsights.Cleaner import cleaner_main
from pyResearchInsights.Analyzer import analyzer_main
from pyResearchInsights.NLP_Engine import nlp_engine_main

'''Abstracts containing these keywords will be queried from Springer'''
keywords_to_search = "Specific tension in human muscle"

'''Calling the pre_processing functions here so that abstracts_log_name and status_logger_name is available across the code.'''
# abstracts_log_name, status_logger_name = pre_processing(keywords_to_search)

'''Runs the scraper here to scrape the details from the scientific repository'''
# scraper_main(keywords_to_search, abstracts_log_name, status_logger_name)



'''The location of the file to be cleaned is mentioned here'''
abstracts_log_name = r"C:/Users/m219613/OneDrive - Mayo Clinic/Documents/Python Scripts/Lit_search2/LOGS/LOG_2022-07-11_11_46_Specific_tension_in_human_muscle/Abstract_Database_2022-07-11_11_46.txt"

'''status_logger() logs the seequence of functions executed during the code run'''
status_logger_name = "Status_Logger_Name"
'''Cleaning the corpus here before any of the other modules use it for analysis'''
cleaner_main(abstracts_log_name, status_logger_name)

'''Calling the Analyzer Function here'''
analyzer_main(abstracts_log_name, status_logger_name)

'''Calling the visualizer code below this portion'''
nlp_engine_main(abstracts_log_name, status_logger_name)