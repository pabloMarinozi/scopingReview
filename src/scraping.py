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
    papers = Paper.objects(Q(inclusion1=True) & Q(inclusion2=True))
    return papers

def citations(phrase):
    link = sch.scholar(phrase[:-1])
    print(link)
    return link

def set_inclusion():
    conectarBd()
    papers = Paper.objects()[0:20]
    print(len(papers))
    for paper in papers:
        paper.inclusion1 = True
        paper.inclusion2 = True
        # print(paper.doi)
        paper.save()

def get_links(url, cont):
    while cont > 0:
        parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
        resp = requests.get(
                url,
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            })
        #soup = BeautifulSoup(resp.text, parser)
        # with open('../output/'+'soup'+str(cont)+'.txt', 'w') as f:
        #     f.write(str(soup))
        # cont = cont - 1
        doi = re.findall("10\.\d{3,9}\/[a-zA-Z0-9-._;():/]+", resp.text)
        doi_clean = set(doi).tolist()
        if len(doi_clean):
            print(doi_clean[0])
            return doi_clean[0]
        else:
            print('error')
            return None

def get_doi(url):
    result = requests.get(
        url,
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    })
    doc = BeautifulSoup(result.text, "html.parser")
    doi = doc.find_all(re.compile("/10.\d{3,9}\/[-._;()/:A-Z0-9]+/i"))

    return doi

def main():
    # phrase = "Early detection of grapevine leafroll disease in a red-berried wine grape cultivar using hyperspectral imaging"
    #set_inclusion()
    papers = get_papers()
    urls = []
    cont = len(papers)
    for paper in papers:
        url = citations(paper.title)
        urls.append(url)
        links = get_links(url, cont)

main()
