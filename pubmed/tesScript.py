import pandas as pd
import time
from bs4 import BeautifulSoup
import seaborn as sns
from matplotlib import pyplot as plt
import itertools
from collections import Counter
from numpy import array_split
from urllib.request import urlopen


# https://towardsdatascience.com/analyze-scientific-publications-with-e-utilities-and-python-56f76de22959
class Searcher:
    # Any instance of searcher will search for the terms and return the number of results on a per year basis #
    def __init__(self, start_, end_, term_, **kwargs):
        self.raw_ = input
        self.name_ = 'searcher'
        self.description_ = 'searcher'
        self.duration_ = end_ - start_
        self.start_ = start_
        self.end_ = end_
        self.term_ = term_
        self.search_results = list()
        self.count_by_year = list()
        self.options = list()

        # Parse keyword arguments

        if 'count' in kwargs and kwargs['count'] == 1:
            self.options = 'rettype=count'

        if 'retmax' in kwargs:
            self.options = f'retmax={kwargs["retmax"]}'

        if 'run' in kwargs and kwargs['run'] == 1:
            self.do_search()
            self.parse_results()

    def do_search(self):
        datestr_ = [self.start_ + x for x in range(self.duration_)]
        options = "".join(self.options)
        for year in datestr_:
            this_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/esearch.fcgi/' + \
                       f'?db=pubmed&term={self.term_}' + \
                       f'&mindate={year}&maxdate={year + 1}&{options}'
            print(this_url)
            self.search_results.append(
                urlopen(this_url).read().decode('utf-8'))
            time.sleep(.33)

    def parse_results(self):
        for result in self.search_results:
            xml_ = BeautifulSoup(result, features="xml")
            self.count_by_year.append(xml_.find('Count').text)
            self.ids = [id.text for id in xml_.find_all('Id')]

    def __repr__(self):
        return repr(f'Search PubMed from {self.start_} to {self.end_} with search terms {self.term_}')

    def __str__(self):
        return self.description

# Create a list which will contain searchers, that retrieve results for each of the search queries
searchers = list()
searchers.append(Searcher(2022, 2023, 'CEO[cois]+OR+CTO[cois]+OR+CSO[cois]', run=1, retmax=10000))
searchers.append(Searcher(2021, 2022, 'CEO[cois]+OR+CTO[cois]+OR+CSO[cois]', run=1, retmax=10000))
searchers.append(Searcher(2020, 2021, 'CEO[cois]+OR+CTO[cois]+OR+CSO[cois]', run=1, retmax=10000))
searchers.append(Searcher(2019, 2020, 'CEO[cois]+OR+CTO[cois]+OR+CSO[cois]', run=1, retmax=10000))
searchers.append(Searcher(2018, 2019, 'CEO[cois]+OR+CTO[cois]+OR+CSO[cois]', run=1, retmax=10000))

# Create a dictionary to store keywords for all articles from a particular year
keywords_dict = dict()

# Each searcher obtained results for a particular start and end year
# Iterate over searchers
for this_search in searchers:

    # Split the results from one search into batches for URL formatting
    chunk_size = 200
    batches = array_split(this_search.ids, len(this_search.ids) // chunk_size + 1)

    # Create a dict key for this searcher object based on the years of coverage
    this_dict_key = f'{this_search.start_}to{this_search.end_}'

    # Each value in the dictionary will be a list that gets appended with keywords for each article
    keywords_all = list()

    for this_batch in batches:
        ids_ = ','.join(this_batch)

        # Pull down the website containing XML for all the results in a batch
        abstract_url = f'http://eutils.ncbi.nlm.nih.gov/entrez//eutils/efetch.fcgi?db=pubmed&id={ids_}'

        abstract_ = urlopen(abstract_url).read().decode('utf-8')
        abstract_bs = BeautifulSoup(abstract_, features="xml")
        articles_iterable = abstract_bs.find_all('PubmedArticle')

        # Iterate over all of the articles from the website
        for article in articles_iterable:
            result = article.find_all('Keyword')
            if result is not None:
                keywords_all.append([x.text for x in result])
            else:
                keywords_all.append([])

        # Take a break between batches!
        time.sleep(1)

    # Once all the keywords are assembled for a searcher, add them to the dictionary
    keywords_dict[this_dict_key] = keywords_all

    # Print the key once it's been dumped to the pickle
    print(this_dict_key)

# Limit to words that appeared approx five times or more in any given year

mapping_ = {'2018to2019':2018,'2019to2020':2019,'2020to2021':2020,'2021to2022':2021,'2022to2023':2022}
global_word_list = list()

for key_,value_ in keywords_dict.items():
  Ntitles = len( value_ )
  flattened_list = list( itertools.chain(*value_) )

  flattened_list = [ x.lower() for x in flattened_list ]
  counter_ = Counter( flattened_list )
  words_this_year = [ ( item , frequency/Ntitles , mapping_[key_] ) for item, frequency in counter_.items() if frequency/Ntitles >= .005 ]
  global_word_list.extend(words_this_year)

# Plot results as clustermap

global_word_df = pd.DataFrame(global_word_list)
global_word_df.columns = ['word', 'frequency', 'year']
pivot_df = global_word_df.loc[:, ['word', 'year', 'frequency']].pivot(index="word", columns="year",
                                                                    values="frequency").fillna(0)

pivot_df.drop('covid-19', axis=0, inplace=True)
pivot_df.drop('sars-cov-2', axis=0, inplace=True)

sns.set(font_scale=0.7)
plt.figure(figsize=(22, 2))
res = sns.clustermap(pivot_df, col_cluster=False, yticklabels=True, cbar=True)