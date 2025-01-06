import logging
import typer
from typing_extensions import Annotated
from enum import Enum
from core.command_metadata import command_metadata
from core.config_manager import initialize_api_connection, initialize_ssh_connection
from tabulate import tabulate
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
def disable_autostart(method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api", verbose: bool = False):
    """
    Disables Autostart of VMs on the ESXi Host
    """
    
    if method.value == "api":
        connection = initialize_api_connection()
        logging.info(f'Sending API request to disable VM autostart')
        payload = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-812e</operationID></Header><Body><ReconfigureAutostart xmlns="urn:vim25"><_this type="HostAutoStartManager">ha-autostart-mgr</_this><spec><defaults><enabled>false</enabled><startDelay>120</startDelay><stopDelay>120</stopDelay><waitForHeartbeat>false</waitForHeartbeat><stopAction>powerOff</stopAction></defaults></spec></ReconfigureAutostart></Body></Envelope>"""
        connection.send_request(payload=payload)
        if verbose:
            ssh_connection = initialize_ssh_connection()
            ssh_connection.retrieve_log('/var/log/hostd.log')
    else:
        connection = initialize_ssh_connection()
        logging.warning('vim-cmd does NOT indicate if the system already had autostart disabled, only if the command was successful.')
        command = f'vim-cmd hostsvc/autostartmanager/enable_autostart false'
        command_output = connection.send_ssh_command(command)
        if 'Disabled AutoStart' in command_output:
            logging.info(f'SSH command {command} executed successfully.')
            if verbose:
                connection.retrieve_log('/var/log/shell.log')
    
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1021.004'], tags=['benign'], methods=['API', 'SSH'])
@app.command()
def enable_ssh(method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api", verbose: bool = False):
    """
    Enables SSH access on the ESXi Host
    """
    if method.value == "api":
        connection = initialize_api_connection()
        logging.info('Sending API request to enable SSH access.')
        payload = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-85b0</operationID></Header><Body><StartService xmlns="urn:vim25"><_this type="HostServiceSystem">serviceSystem</_this><id>TSM-SSH</id></StartService></Body></Envelope>"""
        request = connection.send_request(payload=payload)
        logging.info('Successfully sent request to enable SSH access')
    else:
        connection = initialize_ssh_connection()
        logging.warning('vim-cmd does NOT indicate if following command was successful or not. Verify manually via the ESXi web interface or by attempting an SSH connection.')
        command = f'vim-cmd hostsvc/enable_ssh'
        connection.send_ssh_command(command)
        if verbose:
            connection.retrieve_log('/var/log/shell.log')
    
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1082'], tags=['benign'], methods=['API', 'SSH'])
@app.command()
def get_all_vm_ids(method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api", verbose: bool = False):
    """
    Returns a list of VM ids present on the ESXi Host
    """
    if method.value == "api":
        connection = initialize_api_connection()
        logging.info('Sending API request to enumerate all VM ids.')
        payload = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-90za</operationID></Header><Body><RetrievePropertiesEx xmlns="urn:vim25"><_this type="PropertyCollector">ha-property-collector</_this><specSet><propSet><type>Folder</type><all>false</all><pathSet>childEntity</pathSet></propSet><objectSet><obj type="Folder">ha-folder-vm</obj><skip>false</skip></objectSet></specSet><options/></RetrievePropertiesEx></Body></Envelope>"""
        # get all VM ids
        request = connection.send_request(payload=payload)
        vm_ids = []
        # handle edge case where if a system has 1 VM ESXi returns it as a dict instead of list
        if type(request["soapenv:Envelope"]["soapenv:Body"]["RetrievePropertiesExResponse"]["returnval"]["objects"]["propSet"]["val"]["ManagedObjectReference"]) != list:
            request = [request["soapenv:Envelope"]["soapenv:Body"]["RetrievePropertiesExResponse"]["returnval"]["objects"]["propSet"]["val"]["ManagedObjectReference"]]
        else:
            request = request["soapenv:Envelope"]["soapenv:Body"]["RetrievePropertiesExResponse"]["returnval"]["objects"]["propSet"]["val"]["ManagedObjectReference"]
            
        for vm_id in request:
            id = vm_id["#text"]
            payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-7770</operationID></Header><Body><RetrievePropertiesEx xmlns="urn:vim25"><_this type="PropertyCollector">ha-property-collector</_this><specSet><propSet><type>VirtualMachine</type><all>false</all><pathSet>name</pathSet><pathSet>config</pathSet><pathSet>configIssue</pathSet><pathSet>datastore</pathSet><pathSet>guest</pathSet><pathSet>runtime</pathSet><pathSet>summary.storage</pathSet><pathSet>summary.runtime</pathSet><pathSet>summary.quickStats</pathSet><pathSet>layoutEx</pathSet><pathSet>snapshot</pathSet><pathSet>effectiveRole</pathSet></propSet><objectSet><obj type="VirtualMachine">{id}</obj><skip>false</skip></objectSet></specSet><options/></RetrievePropertiesEx></Body></Envelope>"""
            request = connection.send_request(payload=payload)
            name =  request['soapenv:Envelope']['soapenv:Body']['RetrievePropertiesExResponse']['returnval']['objects']['propSet'][0]['val']['name']
            os_name = request['soapenv:Envelope']['soapenv:Body']['RetrievePropertiesExResponse']['returnval']['objects']['propSet'][0]['val']['guestFullName']
            file = request['soapenv:Envelope']['soapenv:Body']['RetrievePropertiesExResponse']['returnval']['objects']['propSet'][0]['val']['files']['vmPathName']
            vm_ids.append({'id': id, 'name': name, 'os_name': os_name, 'file': file})
        print(tabulate(vm_ids, headers={'id': 'Virtual Machine ID', 'name': 'Virtual Machine Name', 'os_name': 'Operating System', 'file': 'File Path'}, numalign="left"))
    
        