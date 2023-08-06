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
