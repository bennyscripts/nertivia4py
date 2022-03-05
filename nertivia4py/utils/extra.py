AUTH_TOKEN = ""

class Extra:
    def setauthtoken(token):
        global AUTH_TOKEN
        AUTH_TOKEN = token
        
    def getauthtoken():
        global AUTH_TOKEN
        return AUTH_TOKEN