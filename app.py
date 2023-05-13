from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)
API_KEY='e3a053cd179f43b4add5dd0246dd7922'
API_KEY_1='at_PdWcAdzDk3xzCz89dYLStLa3f53tA'

def get_ip(url):
    ip=socket.gethostbyname(url)
    return ip

def get_geoinfo(ip):
    geo_info=requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}&fields=isp,organization,asn,country_code2').json()
    return geo_info

def get_subdomain(url):
    subdomain_resp = requests.get(f'https://subdomains.whoisxmlapi.com/api/v1?apiKey={API_KEY_1}&domainName={url}').json()
    subdomain_resp=subdomain_resp.get('result')['records']
    subdomain=[]
    for response in subdomain_resp:
        result=response.get('domain')
        subdomain.append(result)

    return subdomain

def output(geo_info,subdomain,asset_info):
    final_output='see how'
    return final_output

@app.route('/')
def url_analyzer():
    url=request.args.get('url')
    url = url.replace("https://www.","")

    ip=get_ip(url)
    geo_info=get_geoinfo(ip)
    subdomain=get_subdomain(url)

    return jsonify(geo_info)

# if __name__=='__main__':
#     app.run(debug=True)

