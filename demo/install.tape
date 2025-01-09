# Where should we write the GIF?
Output demo.gif

# Set up a 1200x600 terminal with 46px font.
Set FontSize 23
Set Width 1700
Set Height 800

# Run another command
Type "python3 -m pip install --user pipx"

Enter

Sleep 1s

Type "python3 -m pipx ensurepath --force"

Enter

Sleep 1s

Type "pipx install 'git+https://github.com/AlbinoGazelle/esxi-testing-toolkit.git'"

Enter

Sleep 5s

Type "esxi-testing-toolkit --install-completion"

Enter

Sleep 5s
