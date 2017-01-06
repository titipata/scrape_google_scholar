import re
from bs4 import BeautifulSoup
from unidecode import unidecode

def extract_n_citation(soup):
    """
    Extract number of citations from given PMC BeautifulSoup
    """
    citations_text = soup.find('h2', {'class':'head'}).get_text()
    n_citations = re.sub("Is Cited by the Following ", "", citations_text).split(' ')[0]
    try:
        n_citations = int(n_citations)
    except:
        n_citations = 0
    return n_citations

def extract_article_detail(article):
    """
    Extract information of an articles
    """
    if article.find('span', attrs={'class': 'citation-publication-date'}) is not None:
        date = article.find('span', attrs={'class': 'citation-publication-date'}).get_text().strip()
    else:
        date = ''
    details = article.find('div', attrs={'class': 'details'})
    journal = [text for text in details.find_all(text=True) if text.parent.name != "span"][0].strip()
    if article.find('a', attrs={'class':"view"}) is not None:
        title = article.find('a', attrs={'class':"view"}).text
    else:
        title = ''
    if article.find('span', attrs={'class': 'doi'}) is not None:
        doi = unidecode(article.find('span', attrs={'class': 'doi'}).get_text())
    else:
        doi = ''
    if article.find('div', attrs={'class': 'desc'}) is not None:
        author = article.find('div', attrs={'class': 'desc'}).get_text()
    else:
        author = ''
    pmc_cited = article.find('div', attrs={'class': 'resc'}).dd.text

    dict_cited = {'date': date,
                  'journal': journal,
                  'title': title,
                  'pmc_cited': pmc_cited,
                  'doi': doi,
                  'author': author}
    return dict_cited

def extract_article(html_path):
    """
    Extract details of given PMC article
    """
    soup = BeautifulSoup(open(html_path), 'html.parser')
    pmc = html_path.split('/')[-1].split('.')[0]
    n_citations = extract_n_citation(soup)
    n_pages = int(n_citations/30) + 1
    articles = soup.find_all('div', attrs={'class': 'rprt'})

    url_main = "http://www.ncbi.nlm.nih.gov/pmc/articles/%s/citedby/" % pmc
    alternate_urls = list()
    for i in range(2, n_pages+1):
        url = "http://www.ncbi.nlm.nih.gov/pmc/articles/%s/citedby/?page=%s" % (pmc, str(i))
        alternate_urls.append(url)

    for article in articles:
        dict_cited = extract_article_detail(article)
        if dict_cited['pmc_cited'] == pmc:
            dict_cited['pmc'] = pmc
            dict_cited['url'] = url_main
            dict_cited['n_citations'] = n_citations
            dict_cited['n_pages'] = n_pages
            dict_cited['alternate_url'] = ';'.join(alternate_urls)
            return dict_cited
    return None

def extract_cited_articles(html_path):
    """
    Extract citations list and details of given PMC HTML path
    """
    soup = BeautifulSoup(open(html_path), 'html.parser')
    cited_articles = list()
    pmc = html_path.split('/')[-1].split('.')[0]
    articles = soup.find_all('div', attrs={'class': 'rprt'})
    for article in articles:
        dict_cited = extract_article_detail(article)
        if dict_cited['pmc_cited'] != pmc:
            dict_cited['pmc'] = pmc
            cited_articles.append(dict_cited)
    if len(cited_articles) == 0:
        cited_articles = None
    return cited_articles
