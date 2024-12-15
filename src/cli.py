import typer
from typing import Optional
from core.authenticator import ESXiAuthenticator
from core.connection import ESXiConnection
from core.config_manager import retrieve_secrets

app = typer.Typer()

secrets = retrieve_secrets()

connection = ESXiConnection(
    host=secrets['host'],
    username=secrets['username'],
    password=secrets['password'],
    verify_ssl=False
)

headers = connection.connect()

@app.command()
def hello_world(name: str):
    print(f"Hello {name}")

def main():
    app()
    
if __name__ == "__main__":
    main()