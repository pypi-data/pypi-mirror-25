
class Authenticator(object):
    def authenticate(self):
        pass


class BasicAuthenticator(Authenticator):
    def authenticate(self):
        return 1
