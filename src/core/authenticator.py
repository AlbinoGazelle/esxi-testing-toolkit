# Authentication Handling
import requests
import xmltodict
import typer

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

    def authenticate(self):
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
            
            # Extract SOAP session cookie
            self.session_cookie = response.cookies.get("vmware_soap_session")
            
            if not self.session_cookie:
                raise GeneratorExit("Failed to obtain session cookie")
            
            # Update headers with session cookie
            self.headers.update({
                'Cookie': f'vmware_client=VMWare; vmware_soap_session={self.session_cookie}'
            })
            
            return self.headers
        
        except requests.RequestException as e:
            raise GeneratorExit(f"Authentication failed: {str(e)}")