# Configuration loading 
# via environmental variables or .env files
import os
from dotenv import dotenv_values

def retrieve_secrets():
    """
    Retrieves secrets from .env or environmental variables
    
    :returns: username and password combination
    """
    # if we have a .env file try that first
    if os.path.exists('.env'):
        return retrieve_dotenv()
    else:
        return retrieve_env_vars()

def retrieve_dotenv():
    """
    Retrieves secrets from dotenv file. Assumes ../.env is the correct location.
    
    :returns: ESXI_USERNAME and ESXI_PASSWORD values in ../.env file.
    """
    try:
        secrets = dotenv_values(".env")
        print('get secrets from dotenv')
        return {'username': secrets['ESXI_USERNAME'], 'password': secrets['ESXI_PASSWORD'], "host": secrets['ESXI_HOST']}
    except Exception as e:
        print(f'Cannot retrieve credentials from dotenv file. Falling back to environmental variables {e}')
 
def retrieve_env_vars():
    """
    Retrieves ESXI_USERNAME and ESXI_PASSWORD from environmental variables.
    
    :returns: ESXI_USERNAME and ESXI_PASSWORD enviromental variables.
    :raises: EnvironmentError if it cannot retrieve environmental variables.
    """
    secrets = {}
    try:
        secrets.update({'username': os.environ.get('ESXI_USERNAME')})
        secrets.update({'password': os.environ.get('ESXI_PASSWORD')})
        secrets.update({'host': os.environ.get('ESXI_HOST')})
        print('got secrets from env variables')
        return secrets
    except Exception as e:
        print(f'Cannot get credentials from environmental variables! Exiting')
        raise EnvironmentError