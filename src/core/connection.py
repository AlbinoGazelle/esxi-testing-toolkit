# SOAP API and SSH connection management
import requests
import xmltodict
from core.authenticator import ESXiAuthenticator
class ESXiConnection:
    def __init__(self, host, username, password, verify_ssl=False):
        """
        Manage ESXi host connections and API interactions
        
        :param host: ESXi host IP or hostname
        :param username: ESXi username
        :param password: ESXi password
        :param verify_ssl: SSL Certification verification
        """
        self.authenticator = ESXiAuthenticator(host, username=username, password=password, verify_ssl=verify_ssl)
        self.base_url = f"https://{host}/sdk/"
        self.host = host
        self.headers = None
        
    def connect(self):
        """
        Establishes connection to ESXi host
        
        :return: Authenticated connection headers
        """
        try:
            self.headers = self.authenticator.authenticate()
            print(f"Successfully authenticated to {self.host}. Cookie value is {self.headers['Cookie']}")
        except Exception as e:
            print(f'Error connecting to {self.host}')
            raise ConnectionError