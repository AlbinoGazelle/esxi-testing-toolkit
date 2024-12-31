# import base packages
import typer
import requests
import logging
# import core components
import cli.base_commands
import cli.host_commands
import cli.vm_commands
# used to suppress insecure request warnings from requests
from urllib3.exceptions import InsecureRequestWarning
# suppress insecure request warning for self-signed SSL cert in ESXi hosts.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# logging boilerplate
logger = logging.getLogger(__name__)

FORMAT = '%(asctime)s | %(levelname)-5s | %(message)s'

logging.basicConfig(level=logging.INFO,format=FORMAT)

# typer boilerplate
app = typer.Typer()

# add commands from cli/vm_commands into the app
app.add_typer(cli.vm_commands.app, name="vm", help="Perform actions on Virtual Machines: delete_vm_snapshots | power_off_vm")
app.add_typer(cli.host_commands.app, name="host", help="Performs actions on the ESXi host.")
app.add_typer(cli.base_commands.app, name="base", help="Display information about available tests")

# app entrypoint
def main():
    app()
    
if __name__ == "__main__":
    main()