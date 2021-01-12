#-解析対象となるURLを入力------------
urlinput_start = input('Please enter target URL: ')
#urlinput_start = "https://www.smbc.co.jp/"

@@@@@@@@@@@@
#-解析除隊したいURLキーワード------------
urlinput_del = "facebook\.com|yahoo\.com|youtube\.com|twitter\.com|yahoo\.co\.jp|line\.me"
#-調査階層数------------
# numoflayer = 1
numoflayer = input('Please enter Number of layer for investigation: ')
numoflayer = int(numoflayer)

#利用ヘッダ
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
@@@@@@@@@@@


#Get time stamp for title
import datetime
import socket
from tldextract import extract
import dns.resolver
# import urlparse
from urllib.parse import urlparse
from urllib.parse import urljoin
timestamp = (datetime.datetime.today())
timestamp =(timestamp.strftime("%Y%m%d%H%M"))
filetile = urlparse(urlinput_start).netloc
# print (timestamp)

#必要となるComponentをロード
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count, current_process

import warnings
warnings.filterwarnings('ignore')
import ssl, socket
# import urllib2
import urllib.request
import re
# import urlparse
from urllib.parse import urlparse
from urllib.parse import urljoin
import time
import csv
import numpy
import sys
import shutil
import os
import pandas as pd
from tqdm import tqdm
import pandas as pd
import dns.resolver

from ipwhois import IPWhois
#from pprint import pprint
import warnings
from ipwhois.net import Net
from ipwhois.asn import IPASN
from pprint import pprint
from ipwhois.net import Net
from ipwhois.asn import ASNOrigin
import time



@@@@@@@@@@
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import time

hreflist_mst = pd.DataFrame(columns=[0])

def gethreflist(urlinput):
#     global hreflist
#     global hreflist_mst
#     global hreflist_list
    urlinput_soup = urllib.request.Request(urlinput, headers=hdr)
    html_page = urllib.request.urlopen(urlinput_soup)
    soup = BeautifulSoup(html_page, 'lxml')

    hreflist=[]

    num = 1
    numstr = str(num)

    for link in soup.findAll('a'):
        try:
            href = link.get('href')
            parse_href = urlparse(href)
            hostname = parse_href.netloc
            path = parse_href.path
            path = path.strip()
#             print (href)

        #Hostname無いのもについては、Request URLへの置き換え
            if hostname =='':
#                 print(urlinput)
#                 print(path)

                fullhref = urljoin(urlinput, path)
            else:
                fullhref="https://"+hostname+path
#                 print("else")

            hreflist.append(fullhref)
#             print(fullhref)
        except:
            pass

    hreflist = pd.DataFrame(hreflist)
    hreflist= hreflist[hreflist[0].str.contains("\(*\)|tel\:|\.pdf$|\.zip$|\.exe$|\.csv$|\.docx$|\.doc$|\.xls$|\.xlsx$|@|\.jpg$|\.png$|[0-9]$|\\r\\n")==False]

#     hreflist = hreflist[hreflist[0].str.contains(urlinput_mst)]
    hreflist = hreflist[hreflist[0].str.contains(urlinput_del)==False]
    hreflist = pd.DataFrame(hreflist[0].unique())
    hreflist = hreflist[0].tolist()
#     print (hreflist)
    return hreflist
#Start Curl for layer check
numoflayer = numoflayer -1
hreflistlmst = []
hreflistlayer_current_forexport = pd.DataFrame(index=[])
# data_frame
hreflistlayer_current = gethreflist(urlinput_start)

hreflistlayer_current_len = len(hreflistlayer_current)
# print(hreflistlayer2_len)

print ("---------------------------------------------------------------")
print ("Step1:Start seaching all href links from target URL")
print ("Total number of unique href in layer1:", hreflistlayer_current_len)
print ("")
hreflistlmst = hreflistlayer_current+hreflistlmst

#
countlayer = 1
for var in range(0, numoflayer):
    countlayer = countlayer+1

    hreflistlayer_current_bkup = hreflistlayer_current
    hreflistlayer_current = pd.DataFrame(columns=[0])

    try:
        if not hreflistlayer_current_bkup:
            print ("Layer",countlayer," is last", )
            pass
        else:
            for hreflistlayer_current_href in tqdm(hreflistlayer_current_bkup):
                if hreflistlayer_current_href.upper() and not hreflistlayer_current_href.endswith((".pdf",".xlsx",".docx")):
                    try:
                        hreflistlayer_current_tmp = gethreflist(hreflistlayer_current_href)
                        hreflistlayer_current_tmp = pd.DataFrame(hreflistlayer_current_tmp)
                        hreflistlayercurrent = pd.concat([hreflistlayer_current_tmp, hreflistlayer_current])

                        hreflistlayer_current_forexport_tmp = pd.DataFrame(hreflistlayer_current_tmp)
                        hreflistlayer_current_forexport_tmp['checkedcontent']=hreflistlayer_current_href
                        hreflistlayer_current_forexport = pd.concat([hreflistlayer_current_forexport, hreflistlayer_current_forexport_tmp])

                        time.sleep(1)
                    except:
                        pass
                else:
                    pass

#             hreflistlayer_current = hreflistlayer_current[hreflistlayer_current[0].str.contains(urlinput_mst)]
#             hreflistlayer_current = hreflistlayer_current[hreflistlayer_current[0].str.contains(urlinput_mst)==False]
            hreflistlayer_current = pd.DataFrame(hreflistlayer_current[0].unique())
            hreflistlayer_current = hreflistlayer_current[0].tolist()

            hreflistlayer_current = (list(set(hreflistlayer_current) - set(hreflistlmst)))
            filetile = urlparse(urlinput_start).netloc





            hreflistlmst = hreflistlayer_current+hreflistlmst

            hreflistlayer_current_len = len(hreflistlayer_current)
            # print(hreflistlayer_current_len)
            print ("Total number of unique href in layer",countlayer,":", hreflistlayer_current_len)
            print ("-")
    except:
        pass

try:
    hreflistlmst_list = hreflistlmst.values.tolist()
except:
    hreflistlmst_list = hreflistlmst

print ("---------------------------------------------------------------")
print ("Step2:Start parsing all hreflinks to extract FQDN and exclude duplicated items")

netloc_df = pd.DataFrame(columns=[1])

for origurl in tqdm(hreflistlmst_list):
    origurl = str(origurl).strip('['']')
    origurl = str(origurl).strip('\'\'')
    origurl = str(origurl).strip('\"\"')
    netloc = urllib.parse.urlparse(origurl).netloc
    netlocl_df_tmp = pd.DataFrame([origurl, netloc]).T
    netloc_df = pd.concat([netloc_df, netlocl_df_tmp])

netloc_df = netloc_df.sort_values(1)
netloc_df["number"] = netloc_df.groupby(1).cumcount() + 1
netloc_df = netloc_df[netloc_df['number']==1]

netloc_df.columns = ['OriginalURL', 'FQDN', 'CountNum']

netloc_df


def orgnamechk(hostname):
    try:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
        #s.settimeout(2)
        s.connect((hostname, 443))
        cert = s.getpeercert()
        subject = dict(x[0] for x in cert['subject'])
        answer = subject['organizationName']
    except:
        answer = "N/A"
    return answer




def cnamechk(hostname):
    try:
        dnsresolvquery = dns.resolver.query(hostname, "CNAME")
        for rdata in dnsresolvquery:
            try:
                cname = rdata.target
            except:
                cname = 'N/A'
    except:
        cname = 'N/A'
    return str(cname)
def arecordchk(hostname):
    try:
        dnsresolvquery = dns.resolver.query(hostname, "A")
        for rdata in dnsresolvquery:
            try:
                arecord = rdata.address
            except:
                arecord = 'N/A'
        return str(arecord)
    except:
         arecord = 'N/A'
def asndescchk(hostname):
    try:
        arecord = arecordchk(hostname)
        arec = IPWhois(arecord)
        arecres=arec.lookup_rdap(depth=1)
        ipdesc = arecres["asn_description"]
    except:
        ipdesc = "N/A"
    return ipdesc

def mxrecordchk(hostname):
    try:
        # tsd, td, tsu = extract(hostname) # prints abc, hostname, com
        # domain = td + '.' + tsu # will prints as hostname.com
        mxrecordlist =[]
        for x in dns.resolver.query(hostname, 'MX'):
             mxrecord = str(x.to_text())
             mxrecordlist.append(mxrecord)
        mxrecordlist = ",".join(mxrecordlist)
    except:
        mxrecordlist = "N/A"
    # print(mxrecordlist)
    return mxrecordlist
def nslistchk(hostname):
    try:
        # tsd, td, tsu = extract(hostname) # prints abc, hostname, com
        # domain = td + '.' + tsu # will prints as hostname.com
        nslist =[]
        answers = dns.resolver.query(hostname,'NS')
        for server in answers:
            server = str(server.target)
            nslist.append(server)
        nslist = ",".join(nslist)
    except:
        nslist = "N/A"
    return nslist
def td_tsu_chk(hostname):
    try:
        tsd, td, tsu = extract(hostname) # prints abc, hostname, com
        td_tsu = td + '.' + tsu # will prints as hostname.com
    except:
        td_tsu = "N/A"
    return td_tsu
def mxrecordchk_td_tsu(hostname):
    try:
        tsd, td, tsu = extract(hostname) # prints abc, hostname, com
        domain = td + '.' + tsu # will prints as hostname.com
        mxrecordlist_td_tsu =[]
        for x in dns.resolver.query(domain, 'MX'):
             mxrecord = str(x.to_text())
             mxrecordlist_td_tsu.append(mxrecord)
        mxrecordlist_td_tsu = ",".join(mxrecordlist_td_tsu)
    except:
        mxrecordlist_td_tsu = "N/A"
    # print(mxrecordlist)
    return mxrecordlist_td_tsu
def nslistchk_td_tsu(hostname):
    try:
        tsd, td, tsu = extract(hostname) # prints abc, hostname, com
        domain = td + '.' + tsu # will prints as hostname.com
        nslist_td_tsu =[]
        answers = dns.resolver.query(domain,'NS')
        for server in answers:
            server = str(server.target)
            nslist_td_tsu.append(server)
        nslist_td_tsu = ",".join(nslist_td_tsu)
    except:
        nslist_td_tsu = "N/A"
    # print(nslist)
    return nslist_td_tsu




def checkall(hostname):
#     global result_for_merge_tmp
#     global result_for_merge_tmp
    checkallflag = None
    while checkallflag is None:
        try:
            FQDN_tmp = None
            orgname_tmp = None
            cname_tmp = None
            arecord_tmp = None
            asndesc_tmp = None
            result_for_merge_tmp = None

            mxrecord_tmp = None
            nslist_tmp = None
            td_tsu_tmp = None
            mxrecordchk_td_tsu_tmp = None
            nslist_td_tsu_tmp = None
            FQDN_tmp = hostname
            orgname_tmp = orgnamechk(hostname)
            cname_tmp = cnamechk(hostname)
            arecord_tmp = arecordchk(hostname)
            asndesc_tmp = asndescchk(hostname)
            mxrecord_tmp = mxrecordchk(hostname)
            nslist_tmp = nslistchk(hostname)
            td_tsu_tmp = td_tsu_chk(hostname)
            mxrecordchk_td_tsu_tmp = mxrecordchk_td_tsu(hostname)
            nslist_td_tsu_tmp = nslistchk_td_tsu(hostname)


            result_for_merge_tmp =FQDN_tmp, orgname_tmp, cname_tmp,arecord_tmp,asndesc_tmp,mxrecord_tmp,nslist_tmp,td_tsu_tmp,mxrecordchk_td_tsu_tmp,nslist_td_tsu_tmp
            checkallflag = 1
        except:
            pass
    return result_for_merge_tmp

# FQDNlist = netloc_df['FQDN']
#
# result_for_merge = pd.DataFrame(columns=[1])
#
# lenofFQDNlist = len(FQDNlist)
# print ("Total number of unique FQDN",":", lenofFQDNlist)
#
# for FQDN in tqdm(FQDNlist):
#     result_for_merge_tmp = checkall(FQDN)
#     result_for_merge = pd.concat([result_for_merge, result_for_merge_tmp])
# result_for_merge = result_for_merge.drop(columns=1)
# # result_for_merge
# netloc_df = netloc_df.merge(result_for_merge, on='FQDN', how='left')
FQDNlist = netloc_df['FQDN']
p = Pool()
global result_for_merge_tmp
result_for_merge = pd.DataFrame(columns=[1])

results = []
lenofFQDNlist = len(FQDNlist)
print ("Total number of unique FQDN",":", lenofFQDNlist)

print ("---------------------------------------------------------------")
print ("Step3:Start checking Organization/Cname/Arecord/ASNdesription/MXrecod/NSlist")


for count, result in enumerate(p.imap_unordered(checkall, FQDNlist), 1):
    results.append(result)
    ratio = count/lenofFQDNlist*100
    sys.stdout.write("\r%d%%" % ratio)
    sys.stdout.flush()
p.close()
p.join()

result_for_merge = pd.DataFrame(results)
result_for_merge.columns = ['FQDN', 'Organization', 'Cname','Arecord','ASNdescription','MXrecord','NSrecord','Naked_Domain','Naked_Domain+MXrecord','Naked_Domain+NSlist']
netloc_df = netloc_df.merge(result_for_merge, on='FQDN', how='left')

urlinput_start_fortitle = urllib.parse.urlparse(urlinput_start).netloc

print ("---------------------------------------------------------------")
netloc_df.to_csv(urlinput_start_fortitle+'_'+'WhiteSpaceCheckResult'+'_'+timestamp+'.csv')
print("Completed. Result is saved to "+urlinput_start_fortitle+'_'+'WhiteSpaceCheckResult'+'_'+timestamp+'.csv')
# netloc_df
