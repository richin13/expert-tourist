class APIException(Exception):
    status_code = 400  # Defaults to BadRequest

    def __init__(self, message, status_code=None, **kwargs):
        Exception.__init__(self)
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        self.payload = kwargs

    def to_dict(self):
        r = dict(self.payload or ())
        r['message'] = self.message
        r['status_code'] = self.status_code
        return r
