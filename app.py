from flask import Flask, request, jsonify
from Processing_function import *
from Utils import *

app = Flask(__name__)


@app.route('/')
def url_analyzer():
    url = request.args.get('url')
    domain_suffix, url_suffix = split_url(url)

    ip = get_ip(domain_suffix)
    geo_info = get_geoinfo(ip)
    subdomain = get_subdomain(domain_suffix)
    asset = get_asset(url_suffix, url)

    final = grouped_output(geo_info, subdomain, asset)

    return jsonify(final)
