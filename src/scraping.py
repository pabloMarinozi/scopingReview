from bs4 import BeautifulSoup
import requests
import re

url = "https://www.mdpi.com/1424-8220/21/14/4749"

result = requests.get(
        url,
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
)

doc = BeautifulSoup(result.text, "html.parser")


#10\.1016/j\.infrared\.2021\.103898
#10\.d{3,9}\/[-._;()/:A-Z0-9]+
#10.1016/j.infrared.2021.103898
#/10.\d{3,9}\/[-._;()/:A-Z0-9]+/i
doi = re.findall("10\.\d{3,9}\/[a-zA-Z0-9-._;():/]+", result.text)
doi_clean = set(doi)
print(doi_clean)





