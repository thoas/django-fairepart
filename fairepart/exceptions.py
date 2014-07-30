class BaseFairepartException(Exception):
    pass


class ImportFailed(BaseFairepartException):
    def __init__(self, backend, access_token, *args, **kwargs):
        self.backend = backend
        self.access_token = access_token
        super(ImportFailed, self).__init__(backend, *args, **kwargs)


class ProviderDoesNotExist(BaseFairepartException):
    def __init__(self, backend, *args, **kwargs):
        self.backend = backend
        super(ProviderDoesNotExist, self).__init__(backend, *args, **kwargs)


class MissingParameter(BaseFairepartException):
    def __init__(self, backend, parameter, *args, **kwargs):
        self.backend = backend
        self.parameter = parameter
        super(MissingParameter, self).__init__(backend, *args, **kwargs)
