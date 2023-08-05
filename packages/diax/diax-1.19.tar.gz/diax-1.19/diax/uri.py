import urllib.parse
import uuid

def _maybe_uuid(value):
    try:
        return uuid.UUID(value)
    except:
        pass

def is_uri(value, service=None, path=None):
    url = urllib.parse.urlparse(value)
    if url.scheme != 'https':
        return False
    if service and not service in url.netloc:
        return False
    if path and not url.path.startswith(path):
        return False
    return True

def extract_uuids(value):
    url = urllib.parse.urlparse(value)
    parts = url.path.split('/')
    uuids = [_maybe_uuid(value) for value in parts]
    return [x for x in uuids if x]
