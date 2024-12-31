import logging
from core.config_manager import initialize_api_connection, initialize_ssh_connection
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


@command_metadata(module=['vm'], dependencies=['Virtual Machine with Snapshots'], mitre_attack=['T1485'], tags=['volatile', 'destructive'], methods=['API', 'SSH'])
@app.command()
def delete_vm_snapshots(vm_id: Annotated[str, typer.Argument(help="Virtual Machine ID")], method: Annotated[ExecutionChoice, typer.Argument(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api", verbose: bool = False):
    """
    Deletes all snapshots for a given virtual machine.
    Example: esxi-testing-toolkit vm delete-vm-snapshots 1 ssh
    """
    if method.value == "api":
        connection = initialize_api_connection()
        logging.info(f'Sending API request to delete snapshots for vm: {vm_id}')
        payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-e243</operationID></Header><Body><RemoveAllSnapshots_Task xmlns="urn:vim25"><_this type="VirtualMachine">{vm_id}</_this></RemoveAllSnapshots_Task></Body></Envelope>"""
        request = connection.send_request(payload=payload)
        
        logging.info(f"Task {request['soapenv:Envelope']['soapenv:Body']['RemoveAllSnapshots_TaskResponse']['returnval']['#text']} successful. All snapshots for VM {vm_id} have been deleted.")
        # get hostd logs via SSH here if verbose is enabled
        if verbose:
            logs = connection.retrieve_log('/var/log/hostd.log')
            logging.info(logs)
    elif method.value == "ssh":
        # init SSH connection to ESXi host
        connection = initialize_ssh_connection()
        # send warning about vim-cmd
        logging.warning('vim-cmd does NOT indicate if the snapshot removal was successful or not, only if the VM id exists.')
        # send command
        command = f'vim-cmd vmsvc/snapshot.removeall {vm_id}'
        command_output = connection.send_ssh_command(command)
        # if the VM id that was passed doesn't exist, vim-cmd will produce a vim.fault.NotFound error
        if "vim.fault.NotFound" in command_output:
            logging.error(f'VM Id {vm_id} is not found on the ESXi host.')
            raise SystemExit()
        else:
            logging.info(f'SSH command {command} executed successfully.')
            # get shell.log logs here if erbose is enabled
            if verbose:
                logs = connection.retrieve_log('/var/log/shell.log')
@command_metadata(module=['vm'], dependencies=['Powered On Virtual Machine'], mitre_attack=['T1529'], tags=['volatile'], methods=['API', 'SSH'])
@app.command()
def power_off_vm(vm_id: Annotated[str, typer.Argument(help="Virtual Machine ID")], method: Annotated[ExecutionChoice, typer.Argument(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api"):
    """
    Powers off a VM. 
    Example: esxi-testing-toolkit vm power-off-vm 1 api
    """
    if method.value == "api":
        logging.info(f'Power off VM command is not yet supported! {vm_id}|{method.value}')
        raise NotImplementedError
    else:
        logging.info(f'Power off VM command is not yet supported! {vm_id}|{method.value}')
        raise NotImplementedError
