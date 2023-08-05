import requests

def ping_url(url, timeout=10, proxy=None):
    try :
        requests.get(url,
                     timeout=timeout)
        return True
    except Exception as e:
        print(e.message)
        return False
