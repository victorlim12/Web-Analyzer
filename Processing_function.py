import requests
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlsplit
from urllib.parse import urlparse
import re
from Utils import *

API_KEY = 'e3a053cd179f43b4add5dd0246dd7922'
API_KEY_1 = 'at_PdWcAdzDk3xzCz89dYLStLa3f53tA'


def get_geoinfo(ip):
    geo_info = requests.get(
        f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}&fields=isp,organization,asn,country_code2').json()
    return geo_info


def get_subdomain(url):
    subdomain_resp = requests.get(
        f'https://subdomains.whoisxmlapi.com/api/v1?apiKey={API_KEY_1}&domainName={url}').json()
    subdomain_resp = subdomain_resp.get('result')['records']
    subdomain = []
    for response in subdomain_resp:
        result = response.get('domain')
        subdomain.append(result)

    return subdomain


def get_asset(url_suffix, url):
    output = {
        'anchors': [],
        'iframes': [],
        'images': [],
        'javascripts': [],
        'stylesheets': [],
    }
    html = urlopen(url)
    content = BeautifulSoup(html, 'html.parser')
    for keys in output:
        print(keys)
        if(config.get(keys)[-1] == 'src'):
            temp_result = get_src(content, url_suffix, keys)
            temp_result = checking(temp_result)
            output[keys].extend(temp_result)
        elif (config.get(keys)[-1] == 'href'):
            temp_result = get_href(content, url_suffix, keys)
            temp_result = checking(temp_result)
            output[keys].extend(temp_result)
    return output
