#!/bin/bash -x

# uninstall pipx packages
pipx uninstall-all

# install testing toolkit
pipx install .

# execute tests
esxi-testing-toolkit vm delete-vm-snapshots --vm-id=1 --method=api --verbose

esxi-testing-toolkit vm delete-vm-snapshots --vm-id=1 --method=ssh --verbose

esxi-testing-toolkit vm power-off-vm --vm-id=1 --method=api --verbose

esxi-testing-toolkit vm power-off-vm --vm-id=1 --method=ssh --verbose

esxi-testing-toolkit host disable-autostart --method=ssh --verbose

esxi-testing-toolkit host disable-autostart --method=api --verbose

esxi-testing-toolkit host enable-ssh --method=ssh --verbose

esxi-testing-toolkit host enable-ssh --method=api --verbose

esxi-testing-toolkit host get-all-vm-ids --method=api --verbose