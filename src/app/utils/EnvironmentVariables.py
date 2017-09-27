from os import environ


class EnvironmentVariables:

    def __init__(self):
        self.GOCD_API_URL = environ.get("GOCD_API_URL")
        self.GOCD_USER = environ.get("GOCD_USER")
        self.GOCD_PASSWORD = environ.get("GOCD_PASSWORD")
        self.PORT = environ.get("PORT")

    def gocd_api_url(self):
        return self.GOCD_API_URL

    def gocd_user(self):
        return self.GOCD_USER

    def gocd_password(self):
        return self.GOCD_PASSWORD

    def port(self):
        return int(self.PORT)
