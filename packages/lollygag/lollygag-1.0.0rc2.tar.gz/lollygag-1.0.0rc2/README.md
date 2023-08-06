# Lollygag

## About

* Travis CI: [![Build Status](https://travis-ci.org/snorrwe/lollygag.svg?branch=master)](https://travis-ci.org/snorrwe/lollygag)
* Supported Python versions: 
    * Python 2.7
    * Python 3.6
    * Pypy
    * Pypy 3

## Installation

`pip install lollygag`

## Usage

1. Create a custom _Parser_ to define behaviour
1. Configure the _Crawler_ via either the _run_ method or command line arguments
1. Run your script `python my_crawler.py`

### Sample code

Find the source code [here](https://github.com/snorrwe/lollygag/blob/master/examples/daringer_example.py)

```python
from lollygag import run, Services, LinkParser, DomainCrawler, Crawler


class MyParser(LinkParser):
    def __init__(self, *args, **kwargs):
        super(MyParser, self).__init__(*args, **kwargs)
        self.use_next_data = False

    # on new page is found and shall be processed, 'data' contains full html-source
    def feed(self, data):
        return super(MyParser, self).feed(data)

    # on each start-tag found inside the full html-source
    def handle_starttag(self, tag, attrs):
        # super() will handle links (<a>) parsing, you can add() arbitrary links to self._links
        super(MyParser, self).handle_starttag(tag, attrs)

        # for <script> the contents are needed, set flag to remember it
        if tag == "script":
            self.use_next_data = True
        if tag == "img":
            self.log_service.info("found img: {}".format(dict(attrs).get("src", "<no src attr>")))

    # on each data (between two tags)
    def handle_data(self, data):
        if self.use_next_data:
            self.log_service.info("script contents: {}".format(data))

    # on each end-tag found
    def handle_endtag(self, tag):
        if tag == "script":
            self.use_next_data = False


# `Services.site_parser_factory` defines how a single page is parsed
Services.site_parser_factory = MyParser

# `Services.crawler_factory` defines the Crawler, thus how links are handled (where to crawl?)
# - By default `DomainCrawler` is used, which restricts crawling to _one_ domain
# - You "might" put `Crawler` here, this will lead to endless crawling...
# Services.crawler_factory = Crawler
run()
```

### Command line arguments

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Short</th>
            <th>Description</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <div>
            <tr>
                <td>--help</td>
                <td>-h</td>
                <td rowspan="2">Show the help and exit</td>
                <td> - </td>
            </tr>
            <tr>
            </tr>
        </div>
        <div>
            <tr>
                <td>--url</td>
                <td>-u</td>
                <td rowspan="2">Base url you wish to crawl.<br>
                <i>
                    Note that if you pass the url argument to run() or crawl_domain() this option will be ignored.
                </i>
                </td>
                <td> None </td>
            </tr>
            <tr>
            </tr>
        </div>
        <div>
            <tr>
                <td>--threads</td>
                <td>-t</td>
                <td rowspan="2">Maximum number of concurrent threads</td>
                <td> 5 </td>
            </tr>
            <tr>
            </tr>
        </div>
        <div>
            <tr>
                <td>--loglevel</td>
                <td>-l</td>
                <td rowspan="2">Level of logging, possible values = [all, debug, info, warn, error, none]</td>
                <td> all </td>
            </tr>
            <tr>
            </tr>
        </div>
    </tbody>
</table>

## Contributing

Please refer to the [contribution guidelines](https://github.com/snorrwe/lollygag/blob/master/.github/CONTRIBUTING.md)

## License

[MIT](https://github.com/snorrwe/Crawler/blob/master/LICENSE)
