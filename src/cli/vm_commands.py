import logging
import core.config_manager

def delete_vm_snapshots(vm_id: str):
    """
    Deletes all snapshots for a given VM.
    
    :param: connection: ESXiConnection object.
    :param: vm_id
    :returns: True if successful, False is unsuccessful.
    """
    logging.info(f'Sending request to delete snapshots for vm: {vm_id}')
    payload = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Header><operationID>esxui-e243</operationID></Header><Body><RemoveAllSnapshots_Task xmlns="urn:vim25"><_this type="VirtualMachine">{vm_id}</_this></RemoveAllSnapshots_Task></Body></Envelope>"""
    request = core.config_manager.shared_connection.send_request(payload=payload)