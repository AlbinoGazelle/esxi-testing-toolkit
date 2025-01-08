# Where should we write the GIF?
Output demo.gif

# Set up a 1200x600 terminal with 46px font.
Set FontSize 23
Set Width 1700
Set Height 800

# Run another command
Type "esxi-testing-toolkit host get-all-vm-ids --method=api"

Enter

Sleep 5s

Type "esxi-testing-toolkit vm delete-vm-snapshots --vm-id=1 --method=ssh"

Enter

Sleep 7s
