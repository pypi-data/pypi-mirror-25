"""
Basic web crawling library.
Exports the most common interfaces on the root level.
"""
from lollygag.main import run as run
from lollygag.core.crawlers.domain_crawler import DomainCrawler as DomainCrawler
from lollygag.core.crawlers.crawler import Crawler as Crawler
from lollygag.core.crawlers.mapper_crawler import MapperCrawler as MapperCrawler
from lollygag.services.services import Services as Services
from lollygag.dependency_injection.inject import Inject as Inject
from lollygag.core.parsers.link_parser import ParseResult as ParseResult
from lollygag.core.parsers.link_parser import LinkParser as LinkParser
