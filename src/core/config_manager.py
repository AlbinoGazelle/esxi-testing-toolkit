# Configuration loading 
# via environmental variables or .env files
import os
from dotenv import dotenv_values
import logging

# logger boilerplate
logger = logging.getLogger(__name__)
def retrieve_secrets():
    """
    Retrieves secrets from .env or environmental variables
    
    :returns: username and password combination
    """
    # if we have a .env file try that first
    if os.path.exists('.env'):
        logging.info("Attempting to get secrets from .env file")
        return retrieve_dotenv()
    else:
        logging.info("No .env file found. Attempting to get secrets from environmental variables.")
        return retrieve_env_vars()

def retrieve_dotenv():
    """
    Retrieves secrets from dotenv file. Assumes esxi-testing-toolkit/.env is the correct location.
    
    :returns: ESXI_USERNAME and ESXI_PASSWORD values in .env file.
    """
    try:
        secrets = dotenv_values(".env")
        logging.info("Retrieved configuration information from .env file")
        return {'username': secrets['ESXI_USERNAME'], 'password': secrets['ESXI_PASSWORD'], "host": secrets['ESXI_HOST']}
    except Exception as e:
        logging.info(f'Cannot retrieve credentials from dotenv file. Attempting environmental variables. Error {e}')
 
def retrieve_env_vars():
    """
    Retrieves ESXI_USERNAME and ESXI_PASSWORD from environmental variables.
    
    :returns: ESXI_USERNAME and ESXI_PASSWORD enviromental variables.
    :raises: EnvironmentError if it cannot retrieve environmental variables.
    """
    secrets = {}
    if 'ESXI_USERNAME' in os.environ and 'ESXI_PASSWORD' in os.environ and 'ESXI_HOST' in os.environ:
        secrets.update({'username': os.environ.get('ESXI_USERNAME')})
        secrets.update({'password': os.environ.get('ESXI_PASSWORD')})
        secrets.update({'host': os.environ.get('ESXI_HOST')})
        logging.info("Retrieved configuration information from environmental variables")
        return secrets
    else:
        logging.error(f'Could not retrieve credentials from environmental variables! Please ensure ESXI_USERNAME, ESXI_PASSWORD, and ESXI_HOST environmental variables are set!')
        raise SystemExit()