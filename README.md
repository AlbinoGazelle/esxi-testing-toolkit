<h1>
<p align="center">
&#129520;
<br>ESXi Testing Toolkit
</h1>
  <p align="center">
    Simple and easy to use CLI tool to test ESXi detections.
    <br />
    <a href="#about">About</a>
    ·
    <a href="#installation">Install</a>
    ·
    <a href="#usage">Usage</a>
    ·
    <a href="#detections">Detections</a>
    ·
    <a href="#contribute">Contribute</a>
  </p>
</p>

<gif of toolkit running delete snapshots>

## Disclaimer

>[!CAUTION]  
>ESXi-Testing-Toolkit can modify your ESXi environment to a potentially undesirable state. Please take precautions and only execute it against test environments.

## About

ESXi Testing Toolkit is a command-line utility designed to help security teams test detections deployed in ESXi environments. It takes heavy inspiration from [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) but provides ESXi-specific enhancements and a simpler user experience.

<talk about methods of execution and modules here>


### Tests

After [installing](#installation) the toolkit run the following command to view all available tests, their dependencies, and [MITRE ATT&CK](https://attack.mitre.org/) mappings.

```
esxi-testing-toolkit list all
```


# Installation
Clone the repository and follow one of the supported installation methods.
```
git clone https://github.com/AlbinoGazelle/esxi-testing-toolkit.git
```
## pipx (Recommended)

Install pipx with the following command.
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Use pipx to install esxi-testing-toolkit.
```
cd esxi-testing-toolkit
pipx install .
esxi-testing-toolkit --install-completion
```
Restart shell for command completion.

## pip
```
cd esxi-testing-toolkit
pip install .
esxi-testing-toolkit --install-completion
```
Restart shell for command completion.

# Usage

# Detections
<link to medium blogpost about ESXi detection engineering>
<link to detections/ folder>

# Contribute

# Disclaimer
This tool has the ability to perform destructive actions against ESXi environments. The author has taken neccessary steps, including releasing relevant detections that alert on this tools usage, to help prevent abuse by malicious actors. Please ensure you have permissions from system owners before executing this tool. 