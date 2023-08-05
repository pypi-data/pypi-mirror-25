from lollygag.services.services import Services as S, register_services as rs

Services = S
def register_services(services=None):
    return rs(services)
