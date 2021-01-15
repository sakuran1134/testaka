import sys
import requests
import json
from akamai.edgegrid import EdgeGridAuth
from urllib.parse import urljoin
baseurl = 'https://akab-swugbedetsfo5xvq-wbetycrivce5gswx.luna.akamaiapis.net/'
s = requests.Session()
s.auth = EdgeGridAuth(
client_token='akab-racwk7ais3maiiek-dbjwh4ckaqjkatbt',
client_secret='qxKRTj0nGP2VEU6rfnx5uwXE4r755Kp4rU9XurmOGYQ=',
access_token='akab-2twz2lzoddpyzv3x-mp5piuk5y6ww3rtx'
)

result = s.get(urljoin(baseurl, '/network-list/v2/network-lists?includeElements=truei&extended=true&listType=IP'))
print(result.status_code)
nw_str = json.dumps(result.json())
nw_dict = json.loads(nw_str)

api_uri = nw_dict['networkLists'][0]['links']['retrieve']['href']
nwList_ips = s.get(urljoin(baseurl, api_uri))
print(json.dumps(nwList_ips.json(),indent=2))

#lines = nw_list.readlines()

#l_XXX = [line for line in lines_strip if 'XXX' in line]
#print(l_XXX)


