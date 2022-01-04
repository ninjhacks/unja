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

Unja is a fast & light tool for fetching known URLs from Wayback Machine, Common Crawl, Virus Total & AlienVault's Otx it uses a separate thread for each provider to optimize its speed and use Wayback resumption key to divide scan into multiple parts to handle a large scan & it uses direct filters on API to get only filtered data from API to do less work on your system.

### Why Unja?

- Supports `Wayback/Common-Crawl/Virus-Total/Otx`
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

### How to use Unja?

A detailed usage guide is available on [Usage](https://github.com/ninjhacks/unja/wiki/Usage) section of the Wiki.

Optionally, you can use the `--help` argument to explore Unja on your own.
