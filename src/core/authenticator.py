# Authentication Handling
import requests
import xmltodict
import typer
import logging

# logger boilerplate
logger = logging.getLogger(__name__)

class ESXiAuthenticator:
    def __init__(self, host, username, password, verify_ssl=False):
        """
        Initialize ESXi authenticator with connection parameters
        
        :param host: ESXi host IP or hostname
        :param username: ESXi username 
        :param password: ESXi password
        :param verify_ssl: SSL certificate verification
        """
        
        self.host = host
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        
        self.base_url = f"https://{host}/sdk/"
        self.session_cookie = None
        self.headers = {
            'Content-Type': 'text/xml', 
            'Cookie': 'vmware_client=VMWare', 
            'SOAPAction': 'urn:vim25/7.0.3.0'
        }

    def _build_login_envelope(self):
        """
        Build SOAP login envelope
        
        :return: SOAP XML login request body
        """
        return f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <Header>
                <operationID>esxui-toolkit</operationID>
            </Header>
            <Body>
                <Login xmlns="urn:vim25">
                    <_this type="SessionManager">ha-sessionmgr</_this>
                    <userName>{self.username}</userName>
                    <password>{self.password}</password>
                    <locale>en-US</locale>
                </Login>
            </Body>
        </Envelope>"""

    def authenticate_api(self):
        """
        Authenticate to ESXi host and retrieve session cookie
        
        :return: Authenticated session headers
        :raises AuthenticationError: If authentication fails
        """
        try:
            response = requests.post(
                self.base_url, 
                data=self._build_login_envelope(), 
                headers=self.headers, 
                verify=self.verify_ssl
            )
            
            response.raise_for_status()  # Raise exception for HTTP errors
            
            if not response.cookies.get("vmware_soap_session"):
                logging.error(f'Session cookie not be retrieved from ESXi host. Ensure credentials are correct. Cookies: {response.cookies.items()} Request Response: {response.text}')
                raise SystemExit

            # Extract SOAP session cookie
            self.session_cookie = response.cookies.get("vmware_soap_session")
                        
            # Update headers with session cookie
            self.headers.update({
                'Cookie': f'vmware_client=VMWare; vmware_soap_session={self.session_cookie}'
            })
            
            return self.headers
        # ESXi host isn't reachable
        except requests.exceptions.ConnectionError as e:
            logging.error(f'Could not connect to ESXi host. Ensure the system is reachable and try again: {str(e)}')
            raise SystemExit()
        # ESXi host is reachable but returns HTTP error
        except requests.exceptions.HTTPError as e:
            logging.error(f'Failed to obtain session cookie for {self.username}. Check credentials and try again: {str(e)}')
            raise SystemExit()
        # Anything else
        except requests.exceptions.RequestException as e:
            logging.error(f'Authentication failed. Ensure the ESXi system is reachable and try again {str(e)}')
            raise SystemExit()
    def authenticate_ssh(self):
        """
        Authenticate to ESXi host via SSH.
        
        :return: SSH session
        """
        raise NotImplementedError