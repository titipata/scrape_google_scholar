import re
from bs4 import BeautifulSoup

def get_body(html_page):
    """
    Give path to downloaded Google Scholar html page, return body of given html
    """
    soup = BeautifulSoup(open(html_page), 'html.parser')
    body = soup.find('body')
    return body

def get_user_id(body):
    """
    Get user id from the page
    """
    pub_example = body.find_all('td', attrs={'class': 'gsc_a_t'})[0]
    user_text = pub_example.a['href']
    user_id = re.search('\&user(.*?)\&', user_text).group()[6:-1]
    return user_id

def get_publications(body):
    """
    Give body of html, return all publications
    """
    user_id = get_user_id(body)
    publications = body.find_all('tr', attrs={'class': 'gsc_a_tr'})
    publication_list = list()
    for p in publications:
        pub_details = p.find('td', attrs={'class': 'gsc_a_t'})
        pub_ref = pub_details.a['href']
        pub_meta = pub_details.find_all('div')
        title = pub_details.a.text
        authors = pub_meta[0].text or ''
        journal = pub_meta[1].text or ''
        cited_by = p.find('a', attrs={'class': 'gsc_a_ac'}).text or ''
        year = p.find('span', attrs={'class': 'gsc_a_h'}).text or ''
        pub_dict = {'user_id': user_id,
                    'ref_link': pub_ref,
                    'title': title,
                    'authors': authors,
                    'journal': journal,
                    'cited_by': cited_by,
                    'year': year}
        publication_list.append(pub_dict)
    return publication_list

def get_author_detail(body):
    """
    Give body of Google Scholar html, return details of given author
    """
    user_id = get_user_id(body) # user id
    author_details = body.find('div', {'id': 'gsc_prf_i'})

    name = author_details.find('div', attrs={'id': 'gsc_prf_in'}).text
    name_attributes = author_details.find_all('div', attrs={'class': 'gsc_prf_il'})

    affiliation = name_attributes[0].text or ''
    interests = name_attributes[1].text or ''
    email = name_attributes[2].text or ''

    citation_indices = body.find('table', attrs={'id': 'gsc_rsb_st'})

    year_since_text = citation_indices.find_all('tr')[0]
    year_since = re.sub('Since ', '', year_since_text.find_all('th')[-1].text)

    # citations
    citations = citation_indices.find_all('tr')[1]
    h_index = citation_indices.find_all('tr')[2]
    h_index_all = h_index.find_all('td')[1].text
    h_index_since = h_index.find_all('td')[2].text
    citation_all = citations.find_all('td')[1].text
    citation_since = citations.find_all('td')[2].text

    author_dict = {'user_id': user_id,
                   'name': name,
                   'affiliation': affiliation,
                   'interests': interests,
                   'email': email,
                   'h_index_all': h_index_all,
                   'h_index_since': h_index_since,
                   'citation_all': citation_all,
                   'citation_since': citation_since,
                   'year_since': year_since}
    return author_dict

def get_citations_trend(body):
    """
    Give body of Google Scholar html, return citation per year in table format
    """
    user_id = get_user_id(body)
    citations_per_year = body.find('div', attrs={'id': 'gsc_g'})
    years = citations_per_year.find('div', attrs={'id': 'gsc_g_x'})
    n_citations = citations_per_year.find('div', attrs={'id': 'gsc_g_bars'})
    citations_list = list()
    for year, n_citation in zip(years, n_citations):
        citations_dict = {'user_id': user_id,
                          'n_citation': n_citation.text,
                          'year': year.text}
        citations_list.append(citations_dict)
    return citations_list
