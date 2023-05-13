import socket
import re
import tldextract

config = {
    'anchors': ['a', 'href'],
    'iframes': ['iframe', 'src'],
    'images': ['img', 'src'],
    'javascripts': ['script', 'href'],
    'stylesheets': ['link', 'href'],
}


def get_ip(url):
    ip = socket.gethostbyname(url)
    return ip


def get_src(content, url_suffix, param):
    ext = []
    for link in content.find_all(config.get(param), src=re.compile('^((https://)|(http://))')):
        if 'src' in link.attrs:
            if url_suffix in (link.attrs['src']):
                continue
            else:
                ext.append(link.attrs['src'])
    return ext


def get_href(content, url_suffix, param):
    ext = []
    for link in content.find_all(config.get(param), href=re.compile('^((https://)|(http://))')):
        if 'href' in link.attrs:
            if url_suffix in (link.attrs['href']):
                continue
            else:
                ext.append(link.attrs['href'])
    return ext


def split_url(url):
    ext = tldextract.extract(url)
    domain_suffix = ext.registered_domain
    url_suffix = '.'.join(ext[:3])
    return domain_suffix, url_suffix


def checking(list):
    new = []
    for item in list:
        domain_suffix, url_suffix = split_url(item)
        if url_suffix in new:
            continue
        else:
            new.append(url_suffix)

    return new


def grouped_output(geo_info, subdomain, asset):
    output_config = {
        'info': '',
        'subdomains': '',
        'asset_domains': ''
    }
    output_config.update({'info': geo_info,
                          'subdomains': subdomain,
                          'asset_domains': asset})
    print(output_config)
    return output_config
