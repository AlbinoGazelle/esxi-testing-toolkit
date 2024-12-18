# SOAP API and SSH connection management
import paramiko.client
from core.authenticator import ESXiAuthenticator
import logging
import requests
import xmltodict
import paramiko
from dataclasses import dataclass
import time
# logger boilerplate
logger = logging.getLogger(__name__)

@dataclass
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
        self.password = password
        self.verify_ssh=verify_ssl
        self.authenticator = ESXiAuthenticator(host, username=username, password=password, verify_ssl=verify_ssl)
        self.base_url = f"https://{host}/sdk/"
        self.host = host
        self.headers = None
        self.ssh_conn = None
        
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
        #TODO: ERROR HANDLING WHEN SSH CONNECTION CANNOT BE MADE
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, username=self.username, password=self.password)
        self.ssh_conn = client
        
    def send_ssh_command(self, command: str):
        """
        Sends an SSH command to the ESXi host
        
        :param: command (str): Command to send
        :return: True if successful, False if unsuccessful
        """
        #_stdin, _stdout, _stderr = self.ssh_conn.exec_command(command)
        #print(_stdout.read().decode())
        # need to send command via `invoke_shell` for it to show up in `shell.log` in ESXi system
        shell = self.ssh_conn.invoke_shell()
        # not sure why we need so many sleeps??
        # TODO: ERROR HANDLING WHEN SSH COMMAND FAILS
        time.sleep(1)
        shell.send('echo "execute command with esxi-testing-toolkit"\r\n')
        time.sleep(1)
        shell.send('ls -la\r\n')
        time.sleep(1)
        data = shell.recv(2048)
        print(data.decode())
        
    def send_request(self, payload):
        """
        Sends provided payload to ESXi host
        
        :param: payload
        :return: Response from ESXi host
        """
        try:
            response = requests.post(
                self.base_url,
                data=payload,
                headers=self.headers,
                verify=self.verify_ssh
            )
            response.raise_for_status()
            logging.info(f'Successfully sent request.')
            return True
        except requests.exceptions.ConnectionError as e:
            logging.error(f'Could not connect to ESXi host. Ensure the system is reachable and try again: {str(e)}')
            raise SystemExit()
        # ESXi host is reachable but returns HTTP error
        except requests.exceptions.HTTPError as e:
            logging.error(f'Failed to send payload to {self.host}. Ensure provided details are correct and try again. Error message: {parse_request_error(response.text)}')
            raise SystemExit()
        # Anything else
        except requests.exceptions.RequestException as e:
            logging.error(f'Authentication failed. Ensure the ESXi system is reachable and try again {str(e)}')
            raise SystemExit()
        except Exception as e:
            logging.error(f'Failed to send payload: {e}')
    def return_logs(self, log_file: str, lines: int):
        """
        Returns lines from specific log file to console.
        
        :param: log_file (str): Log file to get lines from.
        :param: lines (int): Number of lines to return.
        """
        logging.error('Returning log from ESXi host is not yet supported!')
        
        # need to use generic SSH connection to pull logs back to stdout
        # ssh_conn = self.connect_ssh()
        # ssh_conn.execute_ssh('cat /var/log/hostd.log')
        raise NotImplementedError
            
def parse_request_error(request_response: str):
    """
    Helper function that parses errors from failed requests.
    
    :param: request_response (str): Response from failed request as a str.
    :return: exact server fault code for failed request
    """
    parsed_response = xmltodict.parse(request_response)
    return parsed_response['soapenv:Envelope']['soapenv:Body']['soapenv:Fault']['faultstring']