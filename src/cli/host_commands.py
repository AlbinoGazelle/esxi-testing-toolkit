import logging
from core.config_manager import initialize_api_connection
import typer
from typing_extensions import Annotated
from enum import Enum
from core.command_metadata import command_metadata

class ExecutionChoice(str, Enum):
    """
    Enum for different methods of executing commands.
    Required for showing default values in Typer command.
    """
    ssh = "ssh"
    api = "api"

# typer boilerplate
app = typer.Typer()

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1529'], tags=['benign'], methods=['API', 'SSH'])
@app.command()
def disable_autostart(method: Annotated[ExecutionChoice, typer.Argument(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api"):
    """
    Disables Autostart of VMs on the ESXi Host
    """
    
    if method.value == "api":
        logging.error('Disable ESXi Host autostart is not yet supported via API!')
        raise NotImplementedError
    else:
        logging.error('Disable ESXi Host autostart is not yet supported via SSH!')
        raise NotImplementedError
    
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1021.004'], tags=['benign'], methods=['API', 'SSH'])
@app.command()
def enable_ssh(method: Annotated[ExecutionChoice, typer.Argument(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api"):
    """
    Enables SSH access on the ESXi Host
    """
    if method.value == "api":
        logging.error(f'Enabling SSH access is not yet supported via {method.value}!')
    else:
        logging.error(f'Enabling SSH access is not yet supported via {method.value}!')
        raise NotImplementedError
    
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1082'], tags=['benign'], methods=['API', 'SSH'])
@app.command()
def get_all_vm_ids(method: Annotated[ExecutionChoice, typer.Argument(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api"):
    """
    Returns a list of VM ids present on the ESXi Host
    """
    raise NotImplementedError