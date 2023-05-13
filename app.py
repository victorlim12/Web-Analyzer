from flask import Flask, request, jsonify, render_template
from Processing_function import *
from Utils import *
from flask_sock import Sock
import json

app = Flask(__name__, template_folder='template')
sock = Sock(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def create_msg(msg):
    response = {'data': ''}
    response['data'] = msg
    return response


@app.route('/')
def url_analyzer():
    url = request.args.get('url')
    domain_suffix, url_suffix = split_url(url)

    ip = get_ip(domain_suffix)
    geo_info = get_geoinfo(ip)
    subdomain = get_subdomain(domain_suffix)
    asset = get_asset(url_suffix, url)

    final = grouped_output(geo_info, subdomain, asset)

    return jsonify(**final)


@app.route('/ws')
def index():
    return render_template('index.html')


@sock.route('/echo')
def echo(sock):
    while True:
        data = sock.receive()
        data = json.loads(data)
        if data.get("url") is not None:
            url = data['url']
            response = create_msg(f'session crated for {url} ')
            domain_suffix, url_suffix = split_url(url)
            ip = get_ip(domain_suffix)
        elif data.get("operation") is not None:
            if(data['operation'] == 'get_info'):
                geo_info = get_geoinfo(ip)
                response = create_msg(f'session crated for {geo_info} ')
            elif(data['operation'] == 'get_subdomains'):
                subdomain = get_subdomain(domain_suffix)
                response = create_msg(f'session crated for {subdomain} ')
            elif(data['operation'] == 'get_asset_domains'):
                asset = get_asset(url_suffix, url)
                response = create_msg(f'session crated for {asset} ')
        sock.send(response)
