import logging
from core.config_manager import initialize_connection
import typer

# typer boilerplate
app = typer.Typer()

@app.command()
def delete_vm_snapshots(vm_id: str):
    """
    Deletes all snapshots for a given VM.
    
    :param: vm_id: ID for the VM you want to power off.
    :returns: True if successful, else False.
    """   
    connection = initialize_connection()
    logging.info(f'Sending request to delete snapshots for vm: {vm_id}')
    payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-e243</operationID></Header><Body><RemoveAllSnapshots_Task xmlns="urn:vim25"><_this type="VirtualMachine">{vm_id}</_this></RemoveAllSnapshots_Task></Body></Envelope>"""
    request = connection.send_request(payload=payload)

@app.command()
def power_off_vm(vm_id: str):
    """
    Powers off a VM.
    
    :param: vm_id: ID for the VM you want to power off.
    :returns: True if successful, else False.
    """
    print(f'Hello world! {vm_id}')