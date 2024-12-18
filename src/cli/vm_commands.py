import logging
from core.config_manager import initialize_api_connection, initialize_ssh_connection
import typer
from typing_extensions import Annotated
from enum import Enum


class ExecutionChoice(str, Enum):
    """
    Enum for different methods of executing commands.
    Required for showing default values in Typer command.
    """
    ssh = "ssh"
    api = "api"

# typer boilerplate
app = typer.Typer()

@app.command()
def delete_vm_snapshots(vm_id: Annotated[str, typer.Argument(help="Virtual Machine ID")], method: Annotated[ExecutionChoice, typer.Argument(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api"):
    """
    Deletes all snapshots for a given virtual machine.
    Example: esxi-testing-toolkit 1 ssh
    """
    
    if method.value == "api":
        connection = initialize_api_connection()
        logging.info(f'Sending API request to delete snapshots for vm: {vm_id}')
        payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-e243</operationID></Header><Body><RemoveAllSnapshots_Task xmlns="urn:vim25"><_this type="VirtualMachine">{vm_id}</_this></RemoveAllSnapshots_Task></Body></Envelope>"""
        request = connection.send_request(payload=payload)
    else:
        # init SSH connection to ESXi host
        connection = initialize_ssh_connection()
        # send command
        connection.send_ssh_command('ls -la')

@app.command()
def power_off_vm(vm_id: Annotated[str, typer.Argument(help="Virtual Machine ID")], method: Annotated[ExecutionChoice, typer.Argument(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api"):
    """
    Powers off a VM. Example: esxi-testing-toolkit 1 api
    """
    if method.value == "api":
        logging.info(f'Power off VM command is not yet supported! {vm_id}|{method.value}')
        raise NotImplementedError
    else:
        logging.info(f'Power off VM command is not yet supported! {vm_id}|{method.value}')
        raise NotImplementedError