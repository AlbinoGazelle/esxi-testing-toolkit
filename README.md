# Overview

ESXi Testing Toolkit is a command-line utility designed to help Detection Engineering teams test detections deployed in ESXi environments. 

The toolkit is split into **vm** and **host** modules. The **vm** module is focused on actions that impact a single virtual machine while the **host** module contains actions that impact the entire ESXi host.


>[!CAUTION]  
>ESXi-Testing-Toolkit modifies your ESXi environment. Please take precautions and only execute it against test environments.

## Execution Methods

<gif of toolkit running delete snapshots>

<git of toolkit running disable autostart>

# Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Use Cases](#use-cases)
- [Detections](#detections)
- [Contribute](#contribute)
- [Disclaimer](#disclaimer)

# Installation

# Usage

# Use Cases
## Host
### Disable VM Autostart
### Enable SSH
### Disable Firewall
### Modify Syslog Configuration
### Disable Coredump Generation

## VM
### Delete VM Snapshots
### Power Off VM

# Detections
<link to medium blogpost about ESXi detection engineering>

# Contribute

## Running Tests

# Disclaimer
This tool has the ability to perform destructive actions against ESXi environments. The author has taken neccessary steps, including releasing relevant detections that alert on this tools usage, to help prevent abuse by malicious actors. Please ensure you have permissions from system owners before executing this tool. 