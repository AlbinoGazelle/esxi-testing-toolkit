- create `retrieve_logs` that retrieves the last X lines from hostd or shell.log and prints to console.
    - pull down log file using SCP or something and send to `PROJECT_DIR/logs` directory. Make sure to modify filename to include a GUID or timestamp.
- Create global session GUID whenever a command is executed. Use GUID when executing commands to include in logs and append to retrieved log files.
    - Go with a shorter GUID
- create `list` command that lists available tests, their dependencies, and MITRE ATT&CK mapping.
    - Need to refactor commands to include a MITRE ATTACK value that can be retrieved easily.
    - Figure out some way to store metadata for commands without using a class. 
        - use decorators. See chat.
    - command should have two options:
        - `esxi-testing-toolkit list vm` -> lists all VM related tests
        - `esxi-testing-toolkit list host` -> lists all host related tests
- add skeleton functions for enumerate all VM ids. 
    - add warning to suggest that users run this command first to see valid VM ids
- Create directory of XML payloads to serve as the basis for correlated commands
    - src/payloads/delete_vm_snapshot.xml -> src/cli/vm_commands.py reads create_vm.xml and uses send_request function to send request.
- Populate README.md
    - Project overview.
    - Use cases.
    - Install instructions
        - Pipx
        - Direct execution
    - Contributions
        - Tests
- Create tests
    - research how
- Create requirements.txt to support direct execution.
    - Integrate into pyproject.toml
- Populate pyproject.toml
    - email
    - description
    - etc