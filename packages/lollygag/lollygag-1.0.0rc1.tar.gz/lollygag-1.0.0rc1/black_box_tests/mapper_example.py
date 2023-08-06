#!/usr/bin/python

from lollygag import run
from lollygag.services import Services
from lollygag.dependency_injection.inject import Inject
from lollygag.core.crawlers.mapper_crawler import MapperCrawler
import json


def on_finish(log_service, crawler):
    def callback(*args):
        log_service.important("-------------Yeah boiiii, done-----------------")
        result = crawler.make_map()
        result = json.dumps(result, indent=4)
        with open("result.json", "w+") as f:
            f.write(result)
        log_service.important("------------Done processing the tree-----------")
    return callback


def main():
    Services.crawler_factory = MapperCrawler
    crawler.on_finish(on_finish(Services.log_service(), crawler))
    run(subscribe={'on_finish': on_finish(Services.log_service())})


if __name__ == '__main__':
    main()
