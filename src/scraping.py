from bs4 import BeautifulSoup
import requests
import scholar as sch
import urllib.request
from crossref_commons.retrieval import get_entity
from crossref_commons.types import EntityType, OutputType
from clases import Paper,Author,Author_Affiliation,Institution,Finantial_Institution
from datosConexion import conectarBd
from mongoengine import Q
from crossref_commons.iteration import iterate_publications_as_json
import re

def get_papers():
    conectarBd()
    papers = Paper.objects(Q(inclusion1=True) & Q(inclusion2=True) & Q(citationsWanted__exists=False))
    return papers

def get_scholarlink(phrase):
    link = sch.scholar(phrase[:-1])
    print(link)
    return link

def get_beautifulsoup(url):
    """ Me devuelve un objeto beautiful soup del url que obtiene como parámetro."""

    parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
    resp = requests.get(
            url,
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        })
    soup = BeautifulSoup(resp.text, parser)

    return soup

def set_inclusion():
    conectarBd()
    papers = Paper.objects()[21:50]
    print(len(papers))
    for paper in papers:
        paper.inclusion1 = True
        paper.inclusion2 = True
        paper.citationsWanted = False
        # print(paper.doi)
        paper.save()

def get_pages(pages):
    """Obtiene los links de todas las páginas de citaciones dado el link de la primer página."""
    bs = pages[0]
    array = bs.find_all('a', class_ = 'gs_nma')
    for row in array:
        aux = get_beautifulsoup('https://scholar.google.com'+row['href'])
        pages.append(aux)
    return pages

def get_links(bs):
    """Navegamos el árbol hasta conseguir todos los links"""
    array = bs.find_all('h3', class_ = 'gs_rt') # gs_or_ggsm
    links = []
    for row in array:
        for a in row.children:
            try:
                links.append(a['href'])
            except:
                pass
    return links


def save_bs(bs):
    """Guardamos la informacion del objeto BeautifulSoup"""
    with open('../output/bs.html', 'w') as f:
        f.write(str(bs))

def get_doi(url):
    result = requests.get(
        url,
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    })
    doi = re.findall("10\.\d{3,9}\/[a-zA-Z0-9-._;():/]+", result.text)
    doi_clean = list(set(doi))
    if len(doi_clean):
        print(doi_clean[0])
        return doi_clean[0]
    else:
        print('error')
        return None

def get_citations(papers):
    # phrase = "Early detection of grapevine leafroll disease in a red-berried wine grape cultivar using hyperspectral imaging"
    #set_inclusion()
    all_dois = set()
    cont = len(papers)
    for paper in papers:
        url = get_scholarlink(paper.title)
        paper.citationsSearched = True
        bs = get_beautifulsoup(url)
        pages = [bs]
        pages = get_pages(pages)
        for page in pages:
            links = get_links(page)
            for link in links:
                dois = get_doi(link)
                paper.citedBy = dois
                all_dois.add(dois)
    return all_dois
