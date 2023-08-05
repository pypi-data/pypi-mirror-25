from xmlrpclib import ServerProxy

class PaperCut:

    def __init__(self, url, token):
        self.server = ServerProxy(url).api
        self._token = token

    def performUserAndGroupSync(self):
        self.server.performUserAndGroupSync(self._token)
