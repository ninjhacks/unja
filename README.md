<h1 align="center">
  <br>
  <a href="https://github.com/ninjhacks/unja"><img style="width:200px" src="https://i.imgur.com/KNeakV9.png" alt="unja"></a>
  <br>
  Unja
  <br>
</h1>

<h4 align="center">Fetch Known Urls</h4>

<p align="center">
  <a href="https://github.com/ninjhacks/unja/releases">
    <img src="https://img.shields.io/github/release/ninjhacks/unja.svg">
  </a>
  <a href="https://pypi.python.org/pypi/unja/">
    <img src="https://img.shields.io/pypi/v/unja.svg">
  </a>
</p>

### What's Unja?

Unja is a fast & light tool for fetching known URLs from Wayback Machine, Common Crawl, Virus Total, UrlScan.io & AlienVault's Otx it uses a separate thread for each provider to optimize its speed and use Wayback resumption key to divide scan into multiple parts to handle a large scan & it uses direct filters on API to get only filtered data from API to do less work on your system.

### Why Unja?

- Supports `Wayback/Common-Crawl/Virus-Total/Otx/UrlScan.io`
- Automatically handles rate limits and timeouts
- Export results: text or detailed output with status,mime,length in JSON
- MultiThreading: separate thread for each provider to fetch data simultaneously
- Filters: apply filters dirtly on provider to avoid unnecessary data

### Installing Unja


You can install `Unja` with pip as following:
```
pip3 install unja
```

or, by downloading this repository and running
```
python3 setup.py install
```

### Updating Unja


You can update `Unja` with pip as following:
```
pip3 install unja -U
```

## Usage

```sh
unja -h
```

This will display help for the tool.

|        Flag       |                      Description                      |                     Example                     |
| :---------------: | :---------------------------------------------------: | :---------------------------------------------: |
|         -d        |                         doimain                       |              unja -d ninjhacks.com              |
|         -f        |        List of domains file seprated by new line      |              unja -f domains.txt                |
|       --sub       |                    Include subdomain                  |              unja --sub                         |
|         -p        | Providers (wayback,commoncrawl,otx,virustotal,urlscan)|              unja -p wayback                    |
|       --wbf       |          (default : statuscode:200 ~mimetype:html)    |              unja --wbf statuscode:200          |
|       --ccf       |          (default : =status:200 ~mime:.*html)         |              unja --ccf =status:200             |
|       --wbl       |      Wayback results per request (default : 10000)    |              unja --wbl 1000                    |
|       --otxl      |         Otx results per request (default : 500)       |              unja --otxl 500                    |
|         -r        |    Amount of retries for http client (default : 3)    |              unja -r 3                          |
|         -v        |           Enable verbose mode to show errors          |              unja -v                            |
|         -j        |  Enable json mode for detailed output in json format  |              unja -j                            |
|         -s        |          Silent mode don't print header               |              unja -s                            |
|       --ucci      |             Update CommonCrawl Index                  |              unja --ucci                        |
|       --vtkey     |         Change VirusTotal Api in config               |              unja --vtkey                       |
|       --uskey     |         Change UrlScan Api in config                  |              unja --uskey                       |

## Output Methods
text = ( default ) Output urls only.

json = ( -j ) Output url,status,mime,length in json format it's can help you later filtering result based on those variables.

## Filters
Filters directly apply on providers to get only useful filtered data from provider.

|      Wayback      |    Commoncrawl    |                      Description                              |
| :---------------: | :---------------: | :-----------------------------------------------------------: |
|statuscode:200     |   =status:200     | return only those urls which status code is 200               |
|!statuscode:200    |   !=status:200    | return only non 200 status code                               |
|mimetype:text/html |  mime:text/html   | return only those url which response type is text/html        |
|!mimetype:text/html|  !=mime:text/html | return only non text/html response type                       |
|~mimetype:html     |   ~mime:.*html    | return all those url which have html word in response type    |
|~original:unja     |   ~url:.*unja     | return all those url which have unja word in url              |

## Oneliners
Get only urls with parameters & status code 200
```
unja -s -d target.com --sub -p wayback,commoncrawl --wbf 'statuscode:200 ~original:=' --ccf '=status:200 ~url:.*=' | anew | tee output
```

Looking for open redirects
```
unja -s -d target.com --sub -p wayback,commoncrawl --wbf '~statuscode:30 ~original:=http' --ccf '~status:30 ~url:.*=http' | anew | tee output
```
Clean result ( Exclude images,css,javascripts,woff & 404)
```
unja -s -d target.com --sub -p wayback,commoncrawl --wbf '!statuscode:404 ~!mimetype:image ~!mimetype:javascript ~!mimetype:css ~!mimetype:woff' --ccf '!=status:404 !~mime:.*image !~mime:.*javascript !~mime:.*css !~mime:.*woff' | anew | tee output
```

Let me know if you have any other good oneliner ./