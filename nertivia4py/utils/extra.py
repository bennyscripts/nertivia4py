AUTH_TOKEN = ""

class Extra:
    def setauthtoken(self):
        global AUTH_TOKEN
        AUTH_TOKEN = self
        
    def getauthtoken():
        global AUTH_TOKEN
        return AUTH_TOKEN