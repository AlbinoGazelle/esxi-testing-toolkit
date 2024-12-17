# import base packages
import typer
import requests
import logging

# import core components
from core.connection import ESXiConnection
from core.config_manager import retrieve_secrets
import core.config_manager
import cli.vm_commands

# used to suppress insecure request warnings from requests
from urllib3.exceptions import InsecureRequestWarning

# suppress insecure request warning for self-signed SSL cert in ESXi hosts.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# logging boilerplate
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)-5s | %(message)s')

# typer boilerplate
app = typer.Typer()

# Get secrets
secrets = retrieve_secrets()

# Attempt connection to ESXi host using provided information
logging.info(f'Attempting to connect to {secrets['host']} as {secrets['username']}')
connection = ESXiConnection(
    host=secrets['host'],
    username=secrets['username'],
    password=secrets['password'],
    verify_ssl=False
)
connection.connect_api()

# push connection to config manager to allow shared use between modules
core.config_manager.shared_connection = connection

# create commands from shared modules
app.command()(cli.vm_commands.delete_vm_snapshots)

# app entrypoint
def main():    
    # start Typer app
    app()
    
if __name__ == "__main__":
    main()