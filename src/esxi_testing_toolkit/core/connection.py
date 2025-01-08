# SOAP API and SSH connection management
import paramiko.client
import paramiko.ssh_exception
import logging
import requests
import xmltodict
import paramiko
import time
import xmltodict
import os
from esxi_testing_toolkit.core.authenticator import ESXiAuthenticator
import uuid

# logger boilerplate
logger = logging.getLogger(__name__)
logging.getLogger('paramiko').setLevel(logging.CRITICAL+1)
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
        self.guid = str(uuid.uuid4()).split('-')[0]
        
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
        try:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, username=self.username, password=self.password)
            self.ssh_conn = client
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            logging.error(f'Error authenticating to {self.host} using SSH. Ensure SSH is enabled and running. {str(e)}')
            raise SystemExit()
        except paramiko.AuthenticationException as e:
            logging.error(f'Error authenticating to {self.host} using provided credentials. Please check supplied credentials and try again. {str(e)}')
            raise SystemExit()
        except paramiko.SSHException as e:
            logging.error(f'Error connecting to {self.host} with SSH. Check to ensure SSH is enabled and running. {str(e)}')
            raise SystemExit()
        except BlockingIOError as e:
            logging.error(f'Error connecting to {self.host} with SSH. Check to ensure SSH is enabled and the host is reachable. {str(e)}')
            raise SystemExit()
        
        
    def send_ssh_command(self, command: str):
        """
        Sends an SSH command to the ESXi host
        
        :param: command (str): Command to send.
        :return: output (str): Output of command that was executed.
        :warning: This function cannot determine if a command was successfully executed or not. You must parse the output and make a determination there.
        """
        # need to send command via `invoke_shell` for it to show up in `shell.log` in ESXi system
        shell = self.ssh_conn.invoke_shell()
        time.sleep(1)
        shell.send('echo "executing command with esxi-testing-toolkit"\r')
        time.sleep(1)
        shell.send(f'{command}\r')
        time.sleep(1)
        output = shell.recv(-1).decode()
        shell.close()
        return output
    
    def retrieve_log(self, log_file: str):
        """
        Uses SSH to retrieve log files from host.
        
        :param: log file full path (/var/log/logfile.log).
        :return: True if successful, raises SystemExit if not.
        """
        # copy logs to local system using scp or something else
        logging.info(f'Retrieving {log_file} from ESXi host.')
        sftp = self.ssh_conn.open_sftp()
        filename = log_file.split('/')[-1]
        local_path = f"{os.getcwd()}/logs/{self.guid}_{filename}"
        try:
            sftp.get(log_file, local_path)
        except FileNotFoundError as e:
            logging.error(f'{log_file} was not found. Cannot retrieve logs automatically: {e}')
            raise SystemExit()
        logging.info(f'{local_path} successfully generated.')
        sftp.close()
        return True
            
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
            return xmltodict.parse(response.text)
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
            
def parse_request_error(request_response: str):
    """
    Helper function that parses errors from failed requests.
    
    :param: request_response (str): Response from failed request as a str.
    :return: exact server fault code for failed request
    """
    parsed_response = xmltodict.parse(request_response)
    return parsed_response['soapenv:Envelope']['soapenv:Body']['soapenv:Fault']['faultstring']