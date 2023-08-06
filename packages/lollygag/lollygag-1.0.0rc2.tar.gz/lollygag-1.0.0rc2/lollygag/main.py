"""
The main module of lollygag.
Holds the run method.
"""
import time
from lollygag.utility.url import get_domain
from lollygag.services import register_services
from lollygag.dependency_injection.inject import Inject


def run(**kwargs):
    """
    Run the crawler.
    All arguments are optional and will fall back to the ConfigService
    if not specified
    Arguments:
        url: url(s) where to start crawling.
        subscribe: method(s) to subscribe to Crawler events.
        crawler: factory method for the desired crawler.
    """
    register_services()
    config = Inject("config_service").request()
    config.setup()
    url = kwargs.get('url', config.urls)
    if len(url) == 1:
        url = url[0]
    subscriber = None
    if 'subscribe' in kwargs:
        subscriber = lambda crawler: subscribe_to_crawler(crawler, **kwargs['subscribe'])
    if not url or not isinstance(url, list):
        crawler = get_crawler(subscriber, **kwargs)
        crawler.crawl(url)
    else:
        url_list_kwargs = {k: kwargs[k] for k in kwargs if k != 'url'}
        crawl_url_list(url, subscriber, **url_list_kwargs)


def crawl_url_list(url, event_register=None, **kwargs):
    """
    Crawls a list of urls.
    Create a crawler instance for each domain found in urls.
    If event_register is present then register it
    on every crawler instance created.
    """
    work_service = Inject('work_service', cache=False).request()
    domains = separate_urls_by_domain(url)
    jobs = Inject("queue").request()
    for domain in domains:
        crawler = get_crawler(event_register, **kwargs)
        crawler.on_finish(lambda *a, **kw: jobs.get())
        job = get_crawl_job(crawler, domains[domain])
        work_service.request_work(job)
        jobs.put(1)
    while not jobs.empty():
        time.sleep(1)


def get_crawl_job(crawler, domain):
    """
    Returns a job representing the crawling of a domain.
    """
    return lambda: crawler.crawl(domain)


def separate_urls_by_domain(urls):
    """
    Spearates urls by domain into a dictionary of lists.
    """
    assert isinstance(urls, list)
    result = {}
    for url in urls:
        domain = get_domain(url)
        if domain not in result:
            result[domain] = []
        result[domain].append(url)
    return result


def get_crawler(subscriber=None, **kwargs):
    """
    Returns a crawler.
    If 'crawler' is not in kwargs use the factory in Services.crawler_factory.
    If subscriber is present then subscribe for events of the crawler.
    """
    factory = kwargs.get('crawler', Inject("crawler_factory", return_factory=True).request())
    crawler = factory()
    if subscriber:
        subscriber(crawler)
    return crawler


def subscribe_to_crawler(crawler, **subscriptions):
    """
    Subscribe to events of the crawler.
    """
    for key in subscriptions:
        assert key in ['on_start', 'on_interrupt', 'on_finish'],\
            "Unrecognised event type=[%s]" % key
        if isinstance(subscriptions[key], list):
            for sub in subscriptions[key]:
                register(crawler, key, sub)
        else:
            register(crawler, key, subscriptions[key])


def register(crawler, event_type, callback):
    """
    Subscribe to the specified event of the crawler.
    """
    assert crawler
    assert callable(callback)
    {
        'on_start': crawler.on_start,
        'on_finish': crawler.on_finish,
        'on_interrupt': crawler.on_interrupt
    }[event_type](callback)
