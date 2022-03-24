#!/usr/bin/env python3

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from threading import Thread
from optparse import OptionParser
import json
import pkg_resources

def wayBack(domain):
    if options.subdomain == True:
        domain = "*."+domain
    try:
        rKey =  True
        resumeKey = ""
        if options.json:
            while rKey:
                wurl = "http://web.archive.org/cdx/search/cdx?url={}/*&collapse=urlkey&output=json&fl=original,statuscode,mimetype,length{}&showResumeKey=true&limit={}&resumeKey={}".format(domain, wbFilters, WBlimit,resumeKey)
                rep = req.get(wurl, stream=True)
                if rep.status_code == 200:
                    if rep.json() != []:
                        if rep.json()[-2] == []:
                            resumeKey = rep.json()[-1][0]
                            
                            for url in rep.json()[1:-2]:
                                print(json.dumps(url))
                        else:
                            rKey = False
                            for url in rep.json()[1:]:
                                print(json.dumps(url))
                    else:
                        rKey = False
                else:
                    rKey = False
        else:
            while rKey:
                wurl = "http://web.archive.org/cdx/search/cdx?url={}/*&collapse=urlkey&output=text&fl=original{}&showResumeKey=true&limit={}&resumeKey={}".format(domain, wbFilters, WBlimit,resumeKey)
                rep = req.get(wurl, stream=True)
                if rep.status_code == 200:
                    data = rep.text.splitlines()
                    if data != []:
                        if len(data) > 1 and data[-2] == "":
                            resumeKey = data[-1]
                            for url in data[1:-2]:
                                print(url)
                        else:
                            rKey = False
                            for url in data:
                                print(url)
                    else:
                        rKey = False
                else:
                    rKey = False
    except requests.RequestException as err:
        if options.verbose:
            print("Error | WayBack | "+str(err))

def commonCrawl(domain):
    if options.subdomain == True:
        domain = "*."+domain
    try:
        if options.json:
            rep = req.get("{}?url={}/*&output=json&fl=url,status,mime,length{}".format(ccIndex,domain, ccFilters))
            if rep.status_code == 200:
                for url in rep.text.splitlines():
                    url = json.loads(url)
                    print(json.dumps([url["url"],url["status"],url["mime"],url["length"]]))
        else:
            rep = req.get("{}?url={}/*&output=text&fl=url{}".format(ccIndex,domain, ccFilters))
            if rep.status_code == 200:
                for url in rep.text.splitlines():
                    print(url)
    except requests.RequestException as err:
        if options.verbose:
            print("Error | commonCrawl | "+str(err))

def Otx(domain):
    try:
        page = 0
        has_next = True
        while has_next:
            page += 1
            otxurl = "https://otx.alienvault.com/api/v1/indicators/domain/{}/url_list?limit={}&page={}".format(domain,OTXlimit,page)
            rep = req.get(otxurl)
            if rep.status_code == 200:
                for url in rep.json()["url_list"]:
                    if options.json:
                        if "httpcode" in url:
                            data = [url["url"],str(url["httpcode"]),"",""]
                        else:
                            data = [url["url"],"","",""]
                        print(json.dumps(data))
                    else:
                        print(url["url"])
                has_next = rep.json()["has_next"]
            else:
                has_next = False
                print("Error | Otx | Response Code "+str(rep.status_code))
    except requests.RequestException as err:
        if options.verbose:
            print("Error | Otx | "+str(err))

def vTotal(domain):
    try:
        vturl = "https://www.virustotal.com/vtapi/v2/domain/report?apikey={}&domain={}".format(vTotalAPI, domain)
        rep = requests.get(vturl)
        if rep.status_code == 200:
            if "detected_urls" in rep.json():
                for url in rep.json()["detected_urls"]:
                    if options.json:
                        print(json.dumps([url['url'],"","",""]))
                    else:
                        print(url['url'])
            if "undetected_urls" in rep.json():
                for url in rep.json()["undetected_urls"]:
                    if options.json:
                        print(json.dumps([url[0],"","",""]))
                    else:
                        print(url[0])
    except requests.RequestException as err:
        if options.verbose:
            print("Error | VirusTotal | "+str(err))

def cCrawlIndex():
    #client = "commonCrawl Index"
    try:
        rep = req.get("http://index.commoncrawl.org/collinfo.json")
        if rep.status_code == 200:
            return rep.json()[0]["cdx-api"]
        else:
            return False
    except:
        return False

def worker(domain):
    if cCrawl:
        Thread(target=commonCrawl, args=(domain,)).start()
    if wBack:
        #wayBack(domain)
        Thread(target=wayBack, args=(domain,)).start()
    if otx:
        Thread(target=Otx, args=(domain,)).start()
    if vtotal:
        Thread(target=vTotal, args=(domain,)).start()

def header():
    print('''\033[01;32m
_____  ______   ________________ 
__  / / /__  | / /_____  /__    |
_  / / /__   |/ /___ _  /__  /| |
/ /_/ / _  /|  / / /_/ / _  ___ |
\____/  /_/ |_/  \____/  /_/  |_|
                                                                                   
Author: sheryar (ninjhacks)
Version : %s

\033[01;37m''' % (__import__('unja').__version__))

parser = OptionParser(usage="%prog: [options]")
parser.add_option( "-d", dest="domain", help="domain (Example : example.com)")
parser.add_option( "--sub", dest="subdomain", action='store_true', help="Subdomain (optional)")
parser.add_option( "-p" , "--providers", dest="providers", default="wayback,commoncrawl,otx,virustotal", help="Select Providers (default : wayback,commoncrawl,otx,virustotal)")
parser.add_option( "--wbf", dest="wbfilter", default="", help="Set filters on wayback api (Example : statuscode:200 ~mimetype:html ~original:=)")
parser.add_option( "--ccf", dest="ccfilter", default="", help="Set filters on commoncrawl api (Example : =status:200 ~mime:.*html ~url:.*=)")
parser.add_option( "--wbl", dest="wbLimit", default=10000, type=int, help="Wayback results per request (default : 10000)")
parser.add_option( "--otxl", dest="otxLimit", default=10000, type=int, help="Otx results per request (default : 500, Max : 500)")
#parser.add_option( "-o", dest="output", help="Output File (optional)")
parser.add_option( "-r", dest="retry", default=3, type=int, help="Amount of retries for http client	 (default : 3)")
parser.add_option( "-v", dest="verbose", action='store_true', help="Enable verbose mode to show errors (optional)")
parser.add_option( "-j", dest="json", action='store_true', help="Enable json mode for detailed output in json format (optional)")
parser.add_option( "-s", dest="silent", action='store_true', help="Silent mode don't print header (optional)")
parser.add_option( "--ucci", dest="ucci", action='store_true', help="Update CommonCrawl Index (optional)")
parser.add_option( "--vtkey", dest="vtkey", default=False, help="Change VirusTotal Api in config (optional)")
(options, args) = parser.parse_args()

if not options.silent:
    header()

retry_strategy = Retry(
    total=options.retry,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods="GET"
)
adapter = HTTPAdapter(max_retries=retry_strategy)
req = requests.Session()
req.mount("https://", adapter)
req.mount("http://", adapter)
req.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
})

configPath = pkg_resources.resource_filename('unja', 'config.json')
configFile = open(configPath, "r")
configData = json.load(configFile)
configFile.close()

if options.ucci:
    newccIndex = cCrawlIndex()
    if newccIndex != False:
        configFile = open(configPath, "w")
        ccIndex = configData["CommonCrawlIndex"] = newccIndex
        json.dump(configData, configFile)
        configFile.close()
    else:
        print("Error | Update commonCrawl Index | Failed")

if options.vtkey:
    configFile = open(configPath, "w")
    ccIndex = configData["VirusTotalApi"] = options.vtkey
    json.dump(configData, configFile)
    configFile.close()

if not options.domain:
    exit()

wbFilters = ccFilters = ""
cCrawl = wBack = otx = vtotal = False
WBlimit = options.wbLimit 
OTXlimit = options.otxLimit

for provider in options.providers.split(','):
    if provider == "commoncrawl":
        ccIndex = configData["CommonCrawlIndex"]
        if ccIndex != "":
            cCrawl = True
        if options.ccfilter != None:    
            for f in options.ccfilter.split():
                ccFilters = ccFilters+"&filter="+f
    elif provider == "wayback":
        wBack = True
        if options.wbfilter != None:    
            for f in options.wbfilter.split():
                wbFilters = wbFilters+"&filter="+f
    elif provider == "otx":
        otx = True
    elif provider == "virustotal":
        if configData["VirusTotalApi"] != "":
            vTotalAPI = configData["VirusTotalApi"]
            vtotal = True
        else:
            if not options.silent:
                print("Warning | VirusTotal | VirusTotal api not found | Use --vtkey")
                exit()

def main():
    if cCrawl | wBack | otx | vtotal:
        worker(options.domain)

if __name__ == "__main__":
    main()