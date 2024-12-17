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

app.add_typer(cli.vm_commands.app, name="vm", help="Perform actions on Virtual Machines: delete_vm_snapshots | power_off_vm")

# app entrypoint
def main():
    app()
    
if __name__ == "__main__":
    main()