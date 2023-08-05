from lollygag.core.domain_crawler import DomainCrawler

def make_node(lst):
    if isinstance(lst, dict):
        return lst
    result = dict()
    for item in lst:
        result[item] = {}
    return result

def get_all_nodes_in_tree(tree):
    result = []
    for node in tree:
        result.append(node)
        if tree[node] and isinstance(tree[node], dict):
            result.extend(get_all_nodes_in_tree(tree[node]))
    return result

def reduce_map(site_map):
    assert isinstance(site_map, dict)
    result = dict(site_map)
    for url in site_map:
        child_nodes = get_all_nodes_in_tree(site_map[url])
        for node in child_nodes:
            if node in result:
                del result[node]
    return result

class MapperCrawler(DomainCrawler):
    def __init__(self, *args, **kwargs):
        super(MapperCrawler, self).__init__(*args, **kwargs)
        self.graph = set()

    def reset(self, url):
        super(MapperCrawler, self).reset(url)
        self.graph = set()

    def process_links(self, origin, links):
        result = super(MapperCrawler, self).process_links(origin, links)
        for link in result:
            self.graph.add((origin, link))
        return result

    def make_map(self):
        result = self.__make_map()
        result = reduce_map(result)
        return result

    def __make_map(self):
        result = {}
        for vertex in self.graph:
            for value in vertex:
                if value not in result:
                    result[value] = {}
            result[vertex[0]][vertex[1]] = result[vertex[1]]
        return result
