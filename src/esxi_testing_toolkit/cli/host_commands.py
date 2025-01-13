import logging
import typer
from typing_extensions import Annotated
from esxi_testing_toolkit.core.command_metadata import command_metadata
from esxi_testing_toolkit.core.config_manager import initialize_api_connection, initialize_ssh_connection, ExecutionChoice, UtilityChoice
from tabulate import tabulate
import re
# typer boilerplate
app = typer.Typer()

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1529'], risk_level=['high'], methods=['API', 'SSH'], utilities=["vim-cmd"], cleanup = ["enable-autostart"])
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
                
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1529'], risk_level=['benign'], methods=['API', 'SSH'], utilities=["vim-cmd"], cleanup = ["disable-autostart"])
@app.command()
def enable_autostart(method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api", verbose: bool = False):
    """
    Enables Autostart of VMs on the ESXi Host
    """
    if method.value == "api":
        connection = initialize_api_connection()
        logging.info(f'Sending API request to enable VM autostart')
        payload = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-812e</operationID></Header><Body><ReconfigureAutostart xmlns="urn:vim25"><_this type="HostAutoStartManager">ha-autostart-mgr</_this><spec><defaults><enabled>true</enabled><startDelay>120</startDelay><stopDelay>120</stopDelay><waitForHeartbeat>false</waitForHeartbeat><stopAction>powerOff</stopAction></defaults></spec></ReconfigureAutostart></Body></Envelope>"""
        connection.send_request(payload=payload)
        if verbose:
            ssh_connection = initialize_ssh_connection()
            ssh_connection.retrieve_log('/var/log/hostd.log')
    else:
        connection = initialize_ssh_connection()
        logging.warning('vim-cmd does NOT indicate if the system already had autostart enabled, only if the command was successful.')
        command = f'vim-cmd hostsvc/autostartmanager/enable_autostart true'
        command_output = connection.send_ssh_command(command)
        if 'Enabled AutoStart' in command_output:
            logging.info(f'SSH command {command} executed successfully.')
            if verbose:
                connection.retrieve_log('/var/log/shell.log')
                
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1021.004'], risk_level=['medium'], methods=['API', 'SSH'], utilities=["vim-cmd"], cleanup = ["disable-ssh"])
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
        command = f'vim-cmd hostsvc/enable_ssh\rvim-cmd hostsvc/start_ssh'
        connection.send_ssh_command(command)
        if verbose:
            connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1021.004'], risk_level=['benign'], methods=['API', 'SSH'], utilities=["vim-cmd"], cleanup = ["enable_ssh"])
@app.command()
def disable_ssh(method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api", verbose: bool = False):
    """
    Disables SSH access on the ESXi Host
    """
    if method.value == "api":
        connection = initialize_api_connection()
        logging.info('Sending API request to disable SSH access.')
        payload = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-85b0</operationID></Header><Body><StopService xmlns="urn:vim25"><_this type="HostServiceSystem">serviceSystem</_this><id>TSM-SSH</id></StopService></Body></Envelope>"""
        request = connection.send_request(payload=payload)
        logging.info('Successfully sent request to disable SSH access')
    else:
        connection = initialize_ssh_connection()
        logging.warning('vim-cmd does NOT indicate if following command was successful or not. Verify manually via the ESXi web interface or by attempting an SSH connection.')
        command = f'vim-cmd hostsvc/disable_ssh\rvim-cmd hostsvc/stop_ssh'
        connection.send_ssh_command(command)
        if verbose:
            connection.retrieve_log('/var/log/shell.log')
        

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1082'], risk_level=['low'], methods=['API', 'SSH'], utilities=["vim-cmd", "esxcli"], cleanup = ["none"])
@app.command()
def get_all_vm_ids(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "vim-cmd", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api",  verbose: bool = False):
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
        # get information on each VM with another API call
        for vm_id in request:
            id = vm_id["#text"]
            payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-7770</operationID></Header><Body><RetrievePropertiesEx xmlns="urn:vim25"><_this type="PropertyCollector">ha-property-collector</_this><specSet><propSet><type>VirtualMachine</type><all>false</all><pathSet>name</pathSet><pathSet>config</pathSet><pathSet>configIssue</pathSet><pathSet>datastore</pathSet><pathSet>guest</pathSet><pathSet>runtime</pathSet><pathSet>summary.storage</pathSet><pathSet>summary.runtime</pathSet><pathSet>summary.quickStats</pathSet><pathSet>layoutEx</pathSet><pathSet>snapshot</pathSet><pathSet>effectiveRole</pathSet></propSet><objectSet><obj type="VirtualMachine">{id}</obj><skip>false</skip></objectSet></specSet><options/></RetrievePropertiesEx></Body></Envelope>"""
            request = connection.send_request(payload=payload)
            name =  request['soapenv:Envelope']['soapenv:Body']['RetrievePropertiesExResponse']['returnval']['objects']['propSet'][0]['val']['name']
            os_name = request['soapenv:Envelope']['soapenv:Body']['RetrievePropertiesExResponse']['returnval']['objects']['propSet'][0]['val']['guestFullName']
            file = request['soapenv:Envelope']['soapenv:Body']['RetrievePropertiesExResponse']['returnval']['objects']['propSet'][0]['val']['files']['vmPathName']
            vm_ids.append({'id': id, 'name': name, 'os_name': os_name, 'file': file})
        print(tabulate(vm_ids, headers={'id': 'Virtual Machine ID', 'name': 'Virtual Machine Name', 'os_name': 'Operating System', 'file': 'File Path'}, numalign="left"))
        
        if verbose:
            connection = initialize_ssh_connection()
            connection.retrieve_log('/var/log/hostd.log')
    elif method.value == "ssh":
        connection = initialize_ssh_connection()
        if utility.value == "vim-cmd":
            command = "vim-cmd vmsvc/getallvms"
        elif utility.value == "esxcli":
            logging.info("ESXCLI can only enumerate running VMs. Use vim-cmd or the API to enumerate both running and non-running.")
            command = "esxcli --formatter=csv --format-param=fields==\"WorldID,DisplayName\" vm process list"
        output = connection.send_ssh_command(command)
        print(output)
        if verbose:
            connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1082'], risk_level=['low'], methods=['SSH'], utilities=["vim-cmd", "esxcli"], cleanup = ["none"])
@app.command()
def get_system_info(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "vim-cmd", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Displays information on the ESXi Host.
    """
    logging.info("Retrieving information on the ESXi host. Information may vary depending on execution method and utility.")
    if method.value == "ssh":
        connection = initialize_ssh_connection()
        if utility.value == "esxcli":
            command = "esxcli system version get\resxcli system hostname get"
            print(connection.send_ssh_command(command))
        elif utility.value == "vim-cmd":
            command = "vim-cmd hostsvc/hostsummary"
            print(connection.send_ssh_command(command))
        if verbose:
            connection.retrieve_log('/var/log/shell.log')
    else:
        logging.error(f"Retrieving system information via {method.value} is not yet supported!")
        raise SystemExit()
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1082'], risk_level=['low'], methods=['API', 'SSH'], utilities=["esxcli"], cleanup = ["none"])
@app.command()
def get_system_users(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "api",  verbose: bool = False):
    """
    Displays a list of users on the ESXi Host.
    """
    if method.value == "api":
        logging.info("Using ESXi API to retrieve a list of ESXi users.")
        connection = initialize_api_connection()
        payload = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-a178</operationID></Header><Body><RetrieveUserGroups xmlns="urn:vim25"><_this type="UserDirectory">ha-user-directory</_this><searchStr></searchStr><exactMatch>false</exactMatch><findUsers>true</findUsers><findGroups>true</findGroups></RetrieveUserGroups></Body></Envelope>"""
        response = connection.send_request(payload=payload)
        users = response['soapenv:Envelope']['soapenv:Body']['RetrieveUserGroupsResponse']['returnval']
        for user in users:
            del user['@xsi:type']
        print(tabulate(users, headers={'principal': 'username', 'fullName': 'name', 'shellAccess': 'Shell Access', 'id': 'id', 'group': 'group'}))
        if verbose:
            connection = initialize_ssh_connection()
            connection.retrieve_log('/var/log/hostd.log')
    elif method.value == "ssh":
        connection = initialize_ssh_connection()
        if utility.value == "esxcli":
            command = "esxcli system account list"
        else:
            logging.error(f"Retrieving the list of ESXi users via {utility.value} is not yet supported!")
            raise SystemExit()
        print(connection.send_ssh_command(command))
        if verbose:
            connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1082'], risk_level=['low'], methods=['SSH'], utilities=["esxcli"], cleanup = ["none"])
@app.command()
def get_system_storage(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    if method.value == "api":
        logging.error(f'Getting system storage information with {method.value} is not yet supported!')
        raise SystemExit()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Getting system storage with {method.value} is not yet supported!")
            raise SystemExit()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli storage filesystem list\resxcli vsan debug vmdk list\resxcli --formatter=csv --format-param=fields==\"Device,DevfsPath\" storage core device list"
            output = connection.send_ssh_command(command=command)
            logging.info(output)
            if verbose:
                connection.retrieve_log('/var/log/shell.log')
                
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1491.001'], risk_level=['low'], methods=['SSH'], utilities=["esxcli"], cleanup = ["none"])
@app.command()
def change_welcome_message(message: Annotated[str, typer.Option(case_sensitive=False, help="Message to update ESXi Welcome Screen to.")], utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    if method.value == "api":
        logging.error(f'Getting system storage information with {method.value} is not yet supported!')
        raise SystemExit()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Changing ESXi welcome message with {method.value} is not yet supported!")
            raise SystemExit()
        else:
            connection = initialize_ssh_connection()
            command = f"esxcli system welcomemsg set -m \"{message}\""
            logging.info(f"Sending {command} to change welcome message to {message}")
            logging.info(connection.send_ssh_command(command=command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1491.001'], risk_level=['critical'], methods=['SSH'], utilities=["esxcli"], cleanup = ["enable-firewall"])
@app.command()
def disable_firewall(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Disables the ESXi firewall
    """
    if method.value == "api":
        logging.error(f"Disabling the ESXi firewall with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Disabling the ESXi firewall with {utility.value} is not yet supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli network firewall set --enabled false"
            logging.info(connection.send_ssh_command(command=command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1491.001'], risk_level=['benign'], methods=['SSH'], utilities=["esxcli"], cleanup = ["disable-firewall"])
@app.command()
def enable_firewall(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Enables the ESXi firewall.
    """
    if method.value == "api":
        logging.error(f"Enabling the ESXi firewall with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Enabling the ESXi firewall with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli network firewall set --enabled true"
            logging.info(connection.send_ssh_command(command=command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1562.004'], risk_level=['critical'], methods=['SSH'], utilities=["esxcli"], cleanup = ["unmodify-firewall"])
@app.command()
def modify_firewall(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Modifies the ESXi firewall to allow all traffic.
    """
    if method.value == "api":
        logging.error(f"Modifying the ESXi firewall with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Modifying the ESXi firewall with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli network firewall set --default-action true"
            logging.info(connection.send_ssh_command(command=command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1562.004'], risk_level=['benign'], methods=['SSH'], utilities=["esxcli"], cleanup = ["modify-firewall"])
@app.command()
def unmodify_firewall(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Unmodifies the ESXi firewall to block matching traffic.
    """
    if method.value == "api":
        logging.error(f"Unmodifying the ESXi firewall with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Unmodifying the ESXi firewall with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli network firewall set --default-action false"
            logging.info(connection.send_ssh_command(command=command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1562.001'], risk_level=['critical'], methods=['SSH'], utilities=["esxcli"], cleanup = ["enable-coredump"])
@app.command()
def disable_coredump(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Disables coredump generation on the ESXi host.
    """
    if method.value == "api":
        logging.error(f"Disabling coredump generation with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Disabling coredump generation with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli system coredump file set --unconfigure"
            logging.info(connection.send_ssh_command(command=command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1562.001'], risk_level=['benign'], methods=['SSH'], utilities=["esxcli"], cleanup = ["disable-coredump"])
@app.command()
def enable_coredump(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Enables coredump generation on the ESXi host.
    """
    if method.value == "api":
        logging.error(f"Enabling coredump generation with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Enabling coredump generation with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            get_path = "esxcli system coredump file list"
            output = connection.send_ssh_command(command=get_path)
            
            try:
                path = re.search(r".*.dumpfile", output).group()
            except AttributeError:
                logging.error('Could not retrieve path to old coredump filepath. Try enabling coredump manually!')
                raise SystemExit()
            
            enable_command = f"esxcli system coredump file set -p={path}"
            
            logging.info(connection.send_ssh_command(enable_command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1590.005'], risk_level=['low'], methods=['SSH'], utilities=["esxcli"], cleanup = ["none"])
@app.command()
def get_network_information(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Gets networking information of the ESXi host.
    """
    if method.value == "api":
        logging.error(f"Getting network information with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Getting network information with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli --formatter=csv network ip interface ipv4 get"
            logging.info(connection.send_ssh_command(command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1562.001'], risk_level=['critical'], methods=['SSH'], utilities=["esxcli"], cleanup = ["restrict_vib_acceptance_level"])
@app.command()
def unrestrict_vib_acceptance_level(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Sets the VIB acceptance level to CommunitySupported
    """
    if method.value == "api":
        logging.error(f"Getting network information with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Getting network information with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli software acceptance set --level CommunitySupported"
            logging.info(connection.send_ssh_command(command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')
                
@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1562.001'], risk_level=['benign'], methods=['SSH'], utilities=["esxcli"], cleanup = ["unrestrict_vib_acceptance_level"])
@app.command()
def restrict_vib_acceptance_level(utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Sets the VIB acceptance level to PartnerSupported (default ESXi setting)
    """
    if method.value == "api":
        logging.error(f"Getting network information with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Getting network information with {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = "esxcli software acceptance set --level PartnerSupported"
            logging.info(connection.send_ssh_command(command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')

@command_metadata(module=['host'], dependencies=['Reachable ESXi System'], mitre_attack=['T1562.001'], risk_level=['critical'], methods=['SSH'], utilities=["esxcli"], cleanup = ["change-syslog-directory"])
@app.command()
def change_syslog_directory(path: Annotated[str, typer.Option(help="Path to change to the new Syslog directory.")], utility: Annotated[UtilityChoice, typer.Option(help="Utility to use when executing. Ignored for non-SSH executions.")] = "esxcli", method: Annotated[ExecutionChoice, typer.Option(case_sensitive=False, help="Method of test execution.", show_choices=True)] = "ssh",  verbose: bool = False):
    """
    Changes the Syslog directory to a supplied path.
    """
    if method.value == "api":
        logging.error(f"Setting the syslog directory with {method.value} is not yet supported!")
        raise NotImplementedError()
    elif method.value == "ssh":
        if utility.value != "esxcli":
            logging.error(f"Setting the syslog directory {utility.value} is not supported!")
            raise NotImplementedError()
        else:
            connection = initialize_ssh_connection()
            command = f"esxcli system syslog config set --logdir={path}"
            logging.info(connection.send_ssh_command(command))
            
            if verbose:
                connection.retrieve_log('/var/log/shell.log')
