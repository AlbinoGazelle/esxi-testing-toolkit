#!/bin/bash -x

# uninstall pipx packages
pipx uninstall-all

# install testing toolkit
pipx install .

# execute tests
esxi-testing-toolkit vm delete-vm-snapshots 1 api

esxi-testing-toolkit vm delete-vm-snapshots 1 ssh