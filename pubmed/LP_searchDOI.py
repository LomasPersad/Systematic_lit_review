import requests
from xml.etree import ElementTree as ET
import random
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen


user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)vAppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
]

user_agent = random.choice(user_agent_list)
# Set the headers
headers = {'User-Agent': user_agent}


def search_pubmed_by_doi(doi):
    if pd.isna(doi):
        return []
    else:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi"

        # Define your query parameters
        params = {
            "db": "pubmed",
            "term": f"{doi}[DOI]",
            "retmode": "xml",
            "api_key": ""
        }

        # Send a GET request to PubMed's ESearch utility
        response = requests.get(search_url, params=params, headers=headers)

        if response.status_code == 200:
            # Parse the XML response
            root = ET.fromstring(response.text)

            # Extract the list of PMIDs
            pmid_list = [element.text for element in root.findall(".//Id")]

            return pmid_list
        else:
            print("Failed to retrieve PubMed IDs.")
            return []


def searchPMIDgetAbstract(ids):
    # get abstract and keywords
    # Split the results from one search into batches for URL formatting
    chunk_size = 200
    batches = np.array_split(ids, len(ids) // chunk_size + 1)

    # Create a dict key for this searcher object based on the years of coverage
    # this_dict_key = f'{this_search.start_}to{this_search.end_}'

    # Each value in the dictionary will be a list that gets appended with keywords for each article
    keywords_all = []

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
    # keywords_dict[this_dict_key] = keywords_all

    # Print the key once it's been dumped to the pickle
    # print(this_dict_key)
    return keywords_all


def searchPMIDgetALL(pmid):

    # Define the base URL for the E-Utilities API
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    # Define the parameters for the E-Utilities API request
    params = {
        "db": "pubmed",
        "id": f"{pmid}[PMID]",
        "retmode": "xml",
        "api_key": "" 
    }

    # Make the API request to retrieve article metadata
    response = requests.get(base_url + "efetch.fcgi",
                            params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response using BeautifulSoup
        soup = BeautifulSoup(response.text, features="xml")

        # Extract metadata from the XML response
        try:
            title = soup.find("ArticleTitle").text
        except:
            print(pmid)
            title = ''
        try:    
            authors = [author.text for author in soup.find_all("Author")]
        except:
            authors=''
          
        abstract = soup.find("AbstractText").text if soup.find(
            "AbstractText") else "N/A"
        try:
            keywords = [keyword.text for keyword in soup.find_all("Keyword")]
        except:
            keywords=''
        try:
            journal = soup.find("Title").text
        except:
            journal = ''
        try:
            volume = soup.find("Volume").text
        except:
            volume = ''
        try:
            issue = soup.find("Issue").text
        except:
            issue = ''
        try:
            pages = soup.find("Pagination").text
        except:
            pages = ''
        try:
            year = soup.find("PubDate").find("Year").text
        except:
            year = ''

        return {
            "Title": title,
            "Authors": authors,
            "Abstract": abstract,
            "Keywords": keywords,
            "Journal": journal,
            "Volume": volume,
            "Issue": issue,
            "Pages": pages,
            "Year": year
        }
    return None


if __name__ == '__main__':

    csv_file = '.\\R\\review_243232_irrelevant_csv_20230909042812.csv'
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    # df = pd.read_csv(csv_file, encoding='ISO-8859-1')
    # ----------Search for PMIDS
    # df['PMID'] = df['DOI'].apply(search_pubmed_by_doi)
    # # df['PMID']
    # csv_filename = '.\\R\\review_243232_irrelevant_csv_20230909042812_pmid.csv'
    # df.to_csv(csv_filename, index=False)
    # --------get ALL
    # data_list = [] 
    # Create an empty DataFrame with columns
    columns = ['Title2', 'Authors2', 'Abstract2','Journal2','Volume2','Issue2','Pages2','Year2','Keywords']
    df_new = pd.DataFrame(columns=columns)
    for index, row in df.iterrows():
        print(row['Title'])
        print('-----------')
        pmid = row['Ref']
        if pd.isna(pmid) == False:
            paper_info = searchPMIDgetALL(pmid)
            if paper_info:
                # Update the DataFrame with the retrieved abstract
                df_new.loc[index, 'Title2'] = paper_info['Title']
                df_new.loc[index, 'Authors2'] = paper_info['Authors'][0] if paper_info['Authors'] else ''
                df_new.loc[index, 'Abstract2'] = paper_info['Abstract']
                df_new.loc[index, 'Journal2'] = paper_info['Journal']
                df_new.loc[index, 'Volume2'] = paper_info['Volume']
                df_new.loc[index, 'Issue2'] = paper_info['Issue']
                df_new.loc[index, 'Pages2'] = paper_info['Pages'] 
                df_new.loc[index, 'Year2'] = int(paper_info['Year']) if paper_info['Year'] else ''
                df_new.loc[index, 'Keywords'] = paper_info['Keywords'][0] if paper_info['Keywords'] else ''
                # data_list.append(paper_info)

            else:
                # Handle cases where no match is found
                # paper_info = {
                #     "Title": 'nan',
                #     "Authors": 'nan',
                #     "Abstract": 'nan',
                #     "Keywords": 'nan',
                #     "Journal": 'nan',
                #     "Volume": 'nan',
                #     "Issue": 'nan',
                #     "Pages": 'nan',
                #     "Year": 'nan'}

                df_new.loc[index, 'Title2'] = 'nan'
                df_new.loc[index, 'Authors2'] = 'nan'
                df_new.loc[index, 'Abstract2'] = 'nan'
                df_new.loc[index, 'Journal2'] = 'nan'
                df_new.loc[index, 'Volume2'] = 'nan'
                df_new.loc[index, 'Issue2'] = 'nan'
                df_new.loc[index, 'Pages2'] = 'nan'
                df_new.loc[index, 'Year2'] = 'nan'
                df_new.loc[index, 'Keywords'] = 'nan'
                # data_list.append(paper_info)
        # df_new = pd.DataFrame(data_list)
        # csv_filename = '.\\R\\review_243232_irrelevant_csv_20230909042812_pmid.csv'
        # df_new.to_csv(csv_filename, index=False)
        time.sleep(5)

    # Create a DataFrame from the list of dictionaries
    # df_new = pd.DataFrame(data_list)

    csv_filename = '.\\R\\review_243232_irrelevant_csv_20230909042812_pmid.csv'
    df_new.to_csv(csv_filename, index=False, encoding='utf-8')
    #

    # search_pubmed_by_doi(doi)# confirm Refs==pmid in csv
