domain_request_method = {
    'forbes.com': 'request_normal',
    'okt.to': 'request_normal',
    'fw.to': 'request_normal',
    'ijnet.org': 'request_normal',
    'fiverr.com': 'request_normal'
}


def get_request_method(domain, default=None):
    return domain_request_method[domain] if domain in domain_request_method else default
