#!/usr/bin/python

from lollygag import run, Services, LinkParser

# Override HTMLParser methods to provide a custom implementation
# https://docs.python.org/2/library/htmlparser.html
# Be sure to call the super methods so you do not lose existing functionality!
#
# Or use a different parser like Beautiful Soup


class MyCrawler(LinkParser):
    def feed(self, data):
        self.log_service.info("Found, a page!")
        return super(MyCrawler, self).feed(data)

    def handle_starttag(self, tag, attrs):
        super(MyCrawler, self).handle_starttag(tag, attrs)
        if tag == 'img':
            self.log_service.info("I found an %s" % tag)
        if tag == 'a':
            self.log_service.debug("I found an anchor tag!")


def on_finish(log_service):
    def callback(*args):
        log_service.info("-------------Yeah boiiii, done-----------------")
    return callback


def main():
    # Override site_parser_factory with my own implementation
    Services.site_parser_factory = MyCrawler
    # Subscribe to events by passing a 'subscribe' dictionary
    run(subscribe={'on_finish': on_finish(Services.log_service())})


if __name__ == '__main__':
    main()
