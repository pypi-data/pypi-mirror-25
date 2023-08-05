import logging
import os

LOGGER = logging.getLogger(__name__)

class UploadError(Exception):
    "Failure to upload data"

def upload(client, filename, type_='stl', name=None):
    name = name or os.path.basename(filename)
    payload = {
        'name'  : name,
        'type'  : type_,
    }
    _, headers = client.post('models', '/model/', payload)
    model = headers['Location']
    upload_url = headers['X-Upload-Location']
    LOGGER.info("Created model %s, uploading data from %s", model, filename)
    with open(filename, 'rb') as f:
        response = client.session.put(upload_url, data=f, headers={'Content-Type': 'application/octet-stream'})
        if not response.ok:
            raise UploadError("Failed to upload model data from {} to {}: {}".format(filename, upload_url, response.text))

    LOGGER.debug("Upload to %s complete", upload_url)
    return model
