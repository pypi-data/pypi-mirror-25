class NotFoundException(Exception):
    status_code = 404

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

