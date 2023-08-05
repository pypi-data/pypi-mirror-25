class DiaxError(Exception):
    "Root exception for anything in diax"

class CredentialsError(DiaxError):
    "Something went wrong with your credentials, likely they weren't provided"

class RequestError(DiaxError):
    "A request to Diax failed in some way"
    def __init__(self, method, url, response):
        super().__init__()
        self.method   = method
        self.response = response
        self.url      = url

    def __str__(self):
        return "RequestError on {} to {} returned {}: {}".format(
            self.method,
            self.url,
            self.response.status_code,
            self.response.text,
        )


class ImpersonationError(DiaxError):
    "Impersonation failed for some reason"

class ValidationError(DiaxError):
    "The request failed validation"

class UserNotFound(DiaxError):
    "The specified users does not exist"
