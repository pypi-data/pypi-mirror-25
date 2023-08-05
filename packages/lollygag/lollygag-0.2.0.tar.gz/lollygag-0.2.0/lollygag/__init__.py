from lollygag.services import register_services, Services

def run(**kwargs):
    register_services()
    crawler = Services.domain_crawler_factory() if "crawler" not in kwargs else kwargs["crawler"]
    url = None if "url" not in kwargs else kwargs["url"]
    crawler.crawl_domain(url)
