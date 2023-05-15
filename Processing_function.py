import requests
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from Utils import *
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_KEY_1 = os.getenv('API_KEY_1')


def get_geoinfo(ip):
    try:
        geo_info = requests.get(
            f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}&fields=isp,organization,asn,country_code2').json()
        return geo_info
    except Exception as e:
        print(e)
        return []


def get_subdomain(url):
    try:
        subdomain_resp = requests.get(
            f'https://subdomains.whoisxmlapi.com/api/v1?apiKey={API_KEY_1}&domainName={url}').json()
        print(subdomain_resp)
        subdomain_resp = subdomain_resp.get('result')['records']
        subdomain = []
        for response in subdomain_resp:
            result = response.get('domain')
            subdomain.append(result)

        return subdomain
    except Exception as e:
        print(e)
        print('error happended at subdomain')
        return []


def get_asset(url_suffix, url):
    try:
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
    except Exception as e:
        print(e)
        print('error at asset retrieval')
        return output
