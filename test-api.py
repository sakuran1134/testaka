import requests
from akamai.edgegrid import EdgeGridAuth
from urllib.parse import urljoin
baseurl = 'https://akab-swugbedetsfo5xvq-wbetycrivce5gswx.luna.akamaiapis.net/'
s = requests.Session()
s.auth = EdgeGridAuth(
client_token='akab-racwk7ais3maiiek-dbjwh4ckaqjkatbt',
client_secret='qxKRTj0nGP2VEU6rfnx5uwXE4r755Kp4rU9XurmOGYQ=',
access_token='akab-2twz2lzoddpyzv3x-mp5piuk5y6ww3rtx'
)

result = s.get(urljoin(baseurl, '/network-list/v2/network-lists?includeElements=true'))
print(result.status_code)
