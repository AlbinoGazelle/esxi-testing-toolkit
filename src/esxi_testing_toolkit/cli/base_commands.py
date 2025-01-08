import typer
from core.command_metadata import get_command_metadata, get_commands_by_module, get_commands_by_mitre
import cli.vm_commands
import cli.host_commands
import cli.host_commands
from tabulate import tabulate

# typer boilerplate
app = typer.Typer()


@app.command()
def list(module: str = typer.Option(default=None), all: bool = False, mitre: str = typer.Option(default=None)):
    """
    Lists toolkit tests.\n
    Examples: \n
        List all tests: esxi-testing-toolkit base list --all\n
        List all tests that map to T1469: esxi-testing-toolkit base list --mitre T1469\n
        List all tests for the VM module: esxi-testing-toolkit base list --module vm\n
        List all tests for the Host module: esxi-testing-toolkit base list --module host\n
    """
    # define print order and header names
    print_order = ['name', 'dependencies', 'module', 'mitre_attack', 'methods', 'risk_level', 'utilities', 'cleanup']
    headers = {'name':'name', 'risk_level': 'risk level', 'dependencies': 'dependencies', 'mitre_attack': 'MITRE ATT&CK', 'method': 'execution methods', 'module': 'module', 'utilities': 'utilities', 'cleanup': 'clean up command'}
    data = []
    if module:
        if module == 'vm':
            commands = get_commands_by_module(tag=module, module=cli.vm_commands)
            for func in commands:
                command_metadata = get_command_metadata(func=func)
                command_metadata.update({'name': func.__name__.replace("_", "-")})
                pretty_data = {k: command_metadata[k] for k in print_order}
                data.append(pretty_data)
        elif module == 'host':
            commands = get_commands_by_module(tag=module, module=cli.host_commands)
            for func in commands:
                command_metadata = get_command_metadata(func=func)
                command_metadata.update({'name': func.__name__.replace("_", "-")})
                pretty_data = {k: command_metadata[k] for k in print_order}
                data.append(pretty_data)
    elif mitre:
        commands = get_commands_by_mitre(mitre_attack=mitre.upper(), module=cli.host_commands) + get_commands_by_mitre(mitre_attack=mitre.upper(), module=cli.vm_commands)
        for func in commands:
            command_metadata = get_command_metadata(func=func)
            command_metadata.update({'name': func.__name__.replace("_", "-")})
            pretty_data = {k: command_metadata[k] for k in print_order}
            data.append(pretty_data)
    elif all:
        # get all commands in both modules
        commands = get_commands_by_module(tag='vm', module=cli.vm_commands) + get_commands_by_module(tag='host', module=cli.host_commands)
        for func in commands:
            command_metadata = get_command_metadata(func=func)
            command_metadata.update({'name': func.__name__.replace("_", "-")})
            pretty_data = {k: command_metadata[k] for k in print_order}
            data.append(pretty_data)
        
    print(tabulate(data, headers=headers, tablefmt='github'))