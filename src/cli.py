# import base packages
import typer
import requests
import logging

# import core components
from core.connection import ESXiConnection
from core.config_manager import retrieve_secrets

# used to suppress insecure request warnings from requests
from urllib3.exceptions import InsecureRequestWarning

# suppress insecure request warning for self-signed SSL cert in ESXi hosts.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# logging boilerplate
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)-5s | %(message)s')

# typer boilerplate
app = typer.Typer()

# Generic CLI command so Typer still works.
@app.command()
def hello_world(name: str):
    print(f"Hello {name}")

# app entrypoint
def main():
    
    # get secrets
    secrets = retrieve_secrets()

    # Attempt connection to ESXi host using provided information
    logger.info(f'Attempting to connect to {secrets['host']} as {secrets['username']}')
    
    connection = ESXiConnection(
        host=secrets['host'],
        username=secrets['username'],
        password=secrets['password'],
        verify_ssl=False
    )
    headers = connection.connect_api()
    
    request = connection.send_request(payload='example')
    # start Typer app
    app()
    
if __name__ == "__main__":
    main()