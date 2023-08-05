import re

def get_protocol(url):
    """
    Returns wether the protocol of the url is http or https
    Returns none if another protocol or no protocol is present in the url
    """
    result = re.search(r"^https?://", url)
    return result.group(0) if result else None

def strip_beginning_slashes(url):
    find = re.search(r"^/+", url)
    if find:
        url = re.sub(find.group(0), "", url)
    return url

def get_domain(url):
    """
    Returns the domain of the given url
    Examples:
        get_domain("http://winnie.thepooh") -> "winnie.thepooh"

        get_domain("http://www.winnie.thepooh") -> "winnie.thepooh"

        get_domain("http://www.winnie.thepooh/") -> "winnie.thepooh"
    """
    assert url is not None
    protocol = get_protocol(url)
    find = re.search(r"(^https?://)?([a-z]|[A-Z]|[0-9]|\.)+/?", url)
    result = None
    if find:
        result = find.group(0)
        if result.endswith("/"):
            result = result[0:-1]
        result = result.replace("www.", "")
        if protocol:
            result = result.replace(protocol, "")
    return result

def is_relative_link(link):
    return not get_protocol(link) and re.search(r"^\.?/([a-z]|[A-Z]|[0-9]|\.)+", link)
