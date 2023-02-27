class EnvCheckerError(Exception):

    def __init__(self, message: object, resolver: object = None, resolving_error: object = None) -> object:
        self.message = message
        self.resolver = resolver
        self.resolving_error = resolving_error

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
