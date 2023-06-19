import tomli

from keystoneauth1 import loading


class CONF:
    def __init__(self):
        self.auth_url = None
        self.password = None
        self.username = None
        self.method = None
        self.application_credential_id = None
        self.application_credential_secret = None

    def load_from_file(self):
        with open(".config/config.toml", "rb") as f:
            config = tomli.load(f)
        self.auth_url = config["keystone"]["auth_url"]
        if config["authentication"]:
            match config["authentication"]:
                case {"method": "ApplicationCredential", "application_credential_id": str(),
                      "application_credential_secret": str()}:
                    self.method = "v3applicationcredential"
                    self.application_credential_id = config["authentication"]["application_credential_id"]
                    self.application_credential_secret = config["authentication"]["application_credential_secret"]
                case {"method": "password", "username": str(), "password": str()}:
                    self.method = "v3password"
                    self.username = config["authentication"]["username"]
                    self.password = config["authentication"]["password"]
                case _:
                    raise Exception("Unknown authentication method")

    def authenticate(self):
        loader = loading.get_plugin_loader(self.method)
        if self.method == "v3applicationcredential":
            return loader.load_from_options(auth_url=self.auth_url,
                                            application_credential_id=self.application_credential_id,
                                            application_credential_secret=self.application_credential_secret)
        elif self.method == "v3password":
            return loader.load_from_options(auth_url=self.auth_url, username=self.username, password=self.password)
