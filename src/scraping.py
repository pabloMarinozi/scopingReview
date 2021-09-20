from bs4 import BeautifulSoup
import requests
import scholar as sch
from crossref_commons.retrieval import get_entity
from crossref_commons.types import EntityType, OutputType
from crossref_commons.iteration import iterate_publications_as_json
import re



def citations(phrase):
    link = sch.scholar(phrase[:-1])
    print(link)
    return link

def get_links(url):
    result = requests.get(
            url,
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        })
    doc = BeautifulSoup(result.text, "html.parser")
    #print(doc.prettify())
    labels = doc.find_all('h3', class_="gs_rt")
    links = []
    for label in labels:
        aux = str(label).split('>')
        aux = aux[8]
        aux = aux.split('=')
        aux= aux[9].split(' ')
        link = aux[0][1:-1]
        links.append(link)
    return links

def get_doi(url):
    result = requests.get(
        url,
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    })
    doc = BeautifulSoup(result.text, "html.parser")
    doi = doc.find_all(re.compile("/^10.\d{4}/\d+-\d+X?(\d+)\d+<[\d\w]+:[\d\w]*>\d+.\d+.\w+;\d$/i"))

    return doi

def main():
    phrase = "Early detection of grapevine leafroll disease in a red-berried wine grape cultivar using hyperspectral imaging"
    url = citations(phrase)
    links = get_links(url)

    dois = []
    for link in links:
        doi = get_doi(link)
        dois.append(doi)

main()
