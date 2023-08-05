import urllib

def encode_url(url):
    '''
    This function takes url string and return encoded url for same
    :param url: string
    :return: string
    PS: urllib.quote convert https: to https%3A and we want to avoid it
        We achieve it by encoding path part separately and merging it with https://
    '''
    url_base, url_path = '', url
    if url.startswith('https://'):
        url_base = 'https://'
        url_path = url.split(url_base, 1)[1]
    elif url.startswith('http://'):
        url_base = 'http://'
        url_path = url.split(url_base, 1)[1]
    return url_base + urllib.quote(url_path)

