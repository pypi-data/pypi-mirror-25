class ServiceUnavailableException(Exception):
    status_code = 503

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
