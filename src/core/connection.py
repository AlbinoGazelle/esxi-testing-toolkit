# SOAP API and SSH connection management
from core.authenticator import ESXiAuthenticator
import logging

# logger boilerplate
logger = logging.getLogger(__name__)

class ESXiConnection:
    def __init__(self, host, username, password, verify_ssl=False):
        """
        Manage ESXi host connections and API interactions
        
        :param host: ESXi host IP or hostname
        :param username: ESXi username
        :param password: ESXi password
        :param verify_ssl: SSL Certification verification
        """
        self.username = username
        self.authenticator = ESXiAuthenticator(host, username=username, password=password, verify_ssl=verify_ssl)
        self.base_url = f"https://{host}/sdk/"
        self.host = host
        self.headers = None
        
    def connect_api(self):
        """
        Establishes connection to ESXi host
        
        :return: Authenticated connection headers
        """
        try:
            self.headers = self.authenticator.authenticate_api()
            logging.info(f"Successfully authenticated to {self.host} as {self.username}")
        except Exception as e:
            logging.error(f'Error connecting to {self.host}: {e}')
            raise SystemExit()
    def connect_ssh(self):
        """
        Establishes a connection to the ESXi host via SSH
        
        :return: SSH session
        """
        raise NotImplementedError
    def send_request(self, payload):
        """
        Sends provided payload to ESXi host
        
        :param: payload
        :return: Response from ESXi host
        """
        print(self.headers)
        