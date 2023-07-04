class AuthenticationError(Exception):

    def __init__(self, Errorinfo):
        super().__init__()
        self.errorinfo = Errorinfo
    def __str__(self):
        return self.errorinfo