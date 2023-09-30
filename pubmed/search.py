import json
import pandas as pd
import lxml
from bs4 import BeautifulSoup
import urllib.request
search_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/esearch.fcgi/' + \
    f'?db=pubmed' + \
    f'&term=myoglobin[mesh]' + \
    f'&mindate=2022' + \
    f'&maxdate=2023' + \
    f'&retmode=json' + \
    f'&retmax=50'

link_list = urllib.request.urlopen(search_url).read().decode('utf-8')
link_list


# Use ESummary to return information about publications
result = json.loads(link_list)
id_list = ','.join(result['esearchresult']['idlist'])

summary_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/esummary.fcgi?db=pubmed&id={id_list}&retmode=json'

summary_list = urllib.request.urlopen(summary_url).read().decode('utf-8')

summary = json.loads(summary_list)
summary['result']['37047528']

uid = [x for x in summary['result'] if x != 'uids']
journals = [summary['result'][x]['fulljournalname']
            for x in summary['result'] if x != 'uids']
titles = [summary['result'][x]['title']
          for x in summary['result'] if x != 'uids']
first_authors = [summary['result'][x]['sortfirstauthor']
                 for x in summary['result'] if x != 'uids']
last_authors = [summary['result'][x]['lastauthor']
                for x in summary['result'] if x != 'uids']
links = [summary['result'][x]['elocationid']
         for x in summary['result'] if x != 'uids']
pubdates = [summary['result'][x]['pubdate']
            for x in summary['result'] if x != 'uids']

links = [re.sub('doi:\s', 'http://dx.doi.org/', x) for x in links]
results_df = pd.DataFrame({'ID': uid, 'Journal': journals, 'PublicationDate': pubdates,
                          'Title': titles, 'URL': links, 'FirstAuthor': first_authors, 'LastAuthor': last_authors})


# Use EFetch when you want abstracts, keywords, and other details (XML output only)
abstract_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/efetch.fcgi?db=pubmed&id={id_list}'
abstract_ = urllib.request.urlopen(abstract_url).read().decode('utf-8')
abstract_bs = BeautifulSoup(abstract_, features="xml")

articles_iterable = abstract_bs.find_all('PubmedArticle')

# Abstracts
abstract_texts = [x.find('AbstractText').text for x in articles_iterable]

# Conflict of Interest statements
coi_texts = [x.find('CoiStatement').text if x.find(
    'CoiStatement') is not None else '' for x in articles_iterable]

# MeSH terms
meshheadings_all = list()
for article in articles_iterable:
    result = article.find('MeshHeadingList').find_all('MeshHeading')
    meshheadings_all.append([x.text for x in result])

# ReferenceList
references_all = list()
for article in articles_:
    if article.find('ReferenceList') is not None:
        result = article.find('ReferenceList').find_all('Citation')
        references_all.append([x.text for x in result])
    else:
        references_all.append([])

results_table = pd.DataFrame({'COI': coi_texts, 'Abstract': abstract_texts,
                             'MeSH_Terms': meshheadings_all, 'References': references_all})


efetch_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/efetch.fcgi?db=pubmed&id={id_list}'
efetch_result = urllib.request.urlopen(efetch_url).read().decode('utf-8')
efetch_bs = BeautifulSoup(efetch_result, features="xml")

tags = efetch_bs.find_all()

for tag in tags:
    print(tag)


# Using ELink to retrieve similar publications, and full-text links

id_ = '37055458'
elink_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/elink.fcgi?db=pubmed&id={id_}&retmode=json&cmd=neighbor_score'
elinks = urllib.request.urlopen(elink_url).read().decode('utf-8')

elinks_json = json.loads(elinks)

ids_ = []
score_ = []
all_links = elinks_json['linksets'][0]['linksetdbs'][0]['links']
for link in all_links:
    [(ids_.append(link['id']), score_.append(link['score']))
     for id, s in link.items()]

pd.DataFrame({'id': ids_, 'score': score_}).drop_duplicates(['id', 'score'])

id_list = '37055458,574140'
elink_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/elink.fcgi?db=pubmed&id={id_list}&retmode=json&cmd=prlinks'
elinks = urllib.request.urlopen(elink_url).read().decode('utf-8')

elinks_json = json.loads(elinks)

elinks_json
urls_ = elinks_json['linksets'][0]['idurllist']
for url_ in urls_:
    [print(url_['id'], x['url']['value']) for x in url_['objurls']]
