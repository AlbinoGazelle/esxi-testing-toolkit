# Where should we write the GIF?
Output list-all-vim.gif

# Set up a 1200x600 terminal with 46px font.
Set FontSize 23
Set Width 1700
Set Height 800

# Run another command
Type "esxi-testing-toolkit host get-all-vm-ids --method=SSH --utility=esxcli"

Enter

Sleep 4s

Type "esxi-testing-toolkit host get-all-vm-ids --method=SSH --utility=vim-cmd"

Enter

Sleep 5s
