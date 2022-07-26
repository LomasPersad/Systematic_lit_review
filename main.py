import requests
import re
from bs4 import BeautifulSoup
#from selenium import webdriver
#import os
import pandas as pd
import time

"""
This is a web scraper for Gscholar. works ok

"""
#header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'} 

#url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C24&inst=12058184521150304743&q=specific+tension+of+human+muscle&btnG='
#response=requests.get(url,headers=headers)

# this function for the getting inforamtion of the web page
def get_paperinfo(paper_url):
  #download the page
  response=requests.get(url,headers=headers)
  # check successful response
  if response.status_code != 200:
    print('Status code:', response.status_code)
    raise Exception('Failed to fetch web page ')
  #parse using beautiful soup
  paper_doc = BeautifulSoup(response.text,'html.parser')
  return paper_doc

# this function for the extracting information of the tags
def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  #cite_tag = doc.select('[title=Cite] + a')
  cite_tag = doc.find_all('div',{"class": "gs_r gs_or gs_scl"})
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})
  return paper_tag,cite_tag,link_tag,author_tag

# it will return the title of the paper
def get_papertitle(paper_tag):  
  paper_names = []  
  for tag in paper_tag:
    paper_names.append(tag.select('h3')[0].get_text())
  return paper_names

# it will return the number of citation of the paper
def get_citecount(cite_tag):
  cite_count = []
  
  for i in cite_tag:
    #cite = i.find_all('div',{'class':'gs_fl'})[1].find_all('a')[2].string
    #cite =  i.find('div',{'class':'gs_ri'}).find_all('a')[4].string
    cite = i.find('div','gs_ri').find('div','gs_fl').find_all('a')[2].string
    print(cite)
    if i is None or cite is None:  # if paper has no citatation then consider 0
      cite_count.append(0)
    else:
      tmp = re.search(r'\d+', cite) # its handle the None type object error and re use to remove the string " cited by " and return only integer value
      if tmp is None :
        cite_count.append(0)
      else :
        cite_count.append(int(tmp.group()))
  return cite_count

# function for the getting link information
def get_link(link_tag):
  links = []
  abstract=[]
  ST_values=[]
  for i in range(len(link_tag)) :
    links.append(link_tag[i].a['href']) 
    #get abstract
    response=requests.get(link_tag[i].a['href'],headers=headers)
    if response.status_code != 200:
        print('Status code:', response.status_code , ' for ',url )
        #raise Exception('Failed to fetch web page ')  
        abs_txt='na'
        sentences='na'      
    else:
        #parse using beautiful soup
        paper_doc = BeautifulSoup(response.text,'html.parser')
        
        if 'journals.physiology.org' in link_tag[i].a['href']:
            class_name="abstractSection abstractInFull"
            
        elif 'link.springer.com' in link_tag[i].a['href']:
            class_name={"c-article-section"}
            
        else:
            class_name={"abstract"}
       
        try:
             #abs_txt=paper_doc.find("div", {"class": class_name}).find('p').text
             abs_txt=paper_doc.find("div", {"class": class_name}).find('p').text.replace('\xa0', '')
             abs_txt=abs_txt.replace('xa0', '').rstrip()
             # now find key words
             words = ['Specific tension', 'kN/m\u00b2']
             sentences = [sentence for sentence in abs_txt.split(".") if any(
             w.lower() in sentence.lower() for w in words)]
             sentences='.'.join(sentences)
             #print(sentences)
             
        except:
             abs_txt='na'
             sentences='na'    
            
    abstract.append(abs_txt)
    ST_values.append(sentences)
    #     print(abs_txt)   
  return links, abstract,ST_values

# function for the getting autho , year and publication information
def get_author_year_publi_info(authors_tag):
  years = []
  publication = []
  authors = []     
  for i in range(len(authors_tag)):
      authortag_text = (authors_tag[i].text).split()
      year = int(re.search(r'\d+', authors_tag[i].text).group())
      years.append(year)
      publication.append(authortag_text[-1])
      author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
      authors.append(author)  
  return years , publication, authors

    
# creating final repository
paper_repos_dict = {
                      'Paper Title' : [],
                      'Year' : [],
                      'Author' : [],
                      'Citation' : [],
                      'Publication' : [],
                      'Url of paper' : [],
                      'Abstract' : [],
                      'key sentences' : []}  
    


# adding information in repository
def add_in_paper_repo(papername,year,author,cite,publi,link,abstract_txt,key_sentence):

  paper_repos_dict['Paper Title'].extend(papername)
  paper_repos_dict['Year'].extend(year)
  paper_repos_dict['Author'].extend(author)
  paper_repos_dict['Citation'].extend(cite)
  paper_repos_dict['Publication'].extend(publi)
  paper_repos_dict['Url of paper'].extend(link)
  paper_repos_dict['Abstract'].extend(abstract_txt)
  paper_repos_dict['key sentences'].extend(key_sentence)

  return pd.DataFrame(paper_repos_dict)





for i in range (0,50,10):

  # get url for the each page
  url = "https://scholar.google.com/scholar?start={}&as_sdt=0%2C24&inst=12058184521150304743&q=specific+tension+of+human+muscle&btnG=".format(i)
  print(url)

  # function for the get content of each page
  doc = get_paperinfo(url)

  # function for the collecting tags
  paper_tag,cite_tag,link_tag,author_tag = get_tags(doc)
  
  # paper title from each page
  papername = get_papertitle(paper_tag)

  # year , author , publication of the paper
  year , publication , author = get_author_year_publi_info(author_tag)

  # cite count of the paper 
  cite = get_citecount(cite_tag)

  # url of the paper
  link, abstract_txt, key_sentence = get_link(link_tag)

  # add in paper repo dict
  #print(len(papername),len(year),len(author),len(cite),len(publication),len(link),len(abstract_txt),len(key_sentence))
  final = add_in_paper_repo(papername,year,author,cite,publication,link,abstract_txt,key_sentence)
  
  # use sleep to avoid status code 429
  time.sleep(5)
  
  #final.to_csv('Specific_tension_papers.csv', sep=',', index=False,header=True)