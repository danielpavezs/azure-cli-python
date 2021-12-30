# Azure VM cloner in Python

## Summary

The main goal is to implement a functionality non developed by Azure or Microsoft yet. Currently, Azure doesn't allow to clone a Virtual Machine (VM), which means, take all the characteristics of a particular VM and create a new VM based on that (same size, location, etc. Same O.S. and same disks with the same data). This **Python code** uses [Azure Command Line Interface](https://docs.microsoft.com/en-us/cli/azure/) (CLI) commands, to manage Azure through the [Azure SDK for Python](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-overview) to **clone a VM**.

## Prerequisites

We need Contributor access to a Tenant in Azure to run some creation/deletion commands (such as `vm create`, `disk create` or `network nsg delete`). The software requirements are:
- **Python 3.8** or higher (a [virtual environment](https://docs.python.org/3/library/venv.html) makes things easier)
- [**pip**](https://pip.pypa.io/en/stable/installation/) (to install the requirements from the `requirements.txt` file)
- [**knack**](https://pypi.org/project/knack/)
- [**packaging**](https://packaging.python.org/en/latest/)
- [**azure-cli**](https://pypi.org/project/azure-cli/)
You can install `knack`, `packaging` and `azure-cli` using pip as follows:
```bash
pip install -r requirements.txt
```
- **Important**: Do not forget to `az login` using your Azure credentials

## Description

This Project consist (for now) of seven files:
1. `main.py`: This file prints the main menu, and asks the user for an option (in the future, there will be more functionalities).
2. `printMessage.py`: This file prints the program header to show the selected path followed by the user
3. `azCliCaller.py`: This file allows us to [call CLI commands](https://github.com/Azure/azure-cli/blob/eace739ce64d793d656067eb9a3c417c6d9285bc/src/azure-cli-core/azure/cli/core/__init__.py#L584) through the [Python SDK](https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-overview), which uses the Azure API to manage Azure resources. So, it's our core file
4. `azVMClone.py`: The file that controls the clone functionality. First, validates if the user wants to clone a VM by searching it, or using the VMs Id.  If the user chooses to use a VM Id, uses that Id to get the original VM data (O.S. disk information, tags, and data disks). If the user chooses to search a VM to clone, it will navigate through the Tenant subscriptions, resource groups and VMs to select a proper VM Id. Over this process, the user will keep informed of the program status through several messages.
5. `azCliDisk.py`: The file that creates a disk (O.S. or data disk) using some data. The main idea is to create an Azure CLI command concatenating flags taken [from the documentation](https://docs.microsoft.com/en-us/cli/azure/disk?view=azure-cli-latest). In that way, if the original disk defines some value to a particular parameter, we'll get it and use it in our disk creation command. This file also defines the [function that attaches](https://docs.microsoft.com/en-us/cli/azure/vm/disk?view=azure-cli-latest) a disk to a VM.
6. `azCliTag.py`: The file that gets the tags from an original resource and creates a command that allows to copy them to a cloned resource. Notice that if the tag-key or value uses the character `~`, this will fail. Be careful and change it if it's possible.
7. `azCliVM.py`: Similar to `azCliDisk.py` this file would concatenate the `az vm create` [parameters](https://docs.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest) to create a proper VM cloner command. The creation command always creates a VM with a [network security group (NSG)](https://docs.microsoft.com/en-us/cli/azure/network/nsg?view=azure-cli-latest) and a [public network](https://docs.microsoft.com/en-us/cli/azure/network/public-ip?view=azure-cli-latest) so, if the original VM doesn't have one of these characteristics, there would be deleted after the VM's creation.

## Usage

The steps to use this code are the following:

1. Run the `main.py` code, no parameters are required
```bash
python3 main.py
```
2. The program will show the main menu where you can clone a VM or exit
```bash
###################################
# VMs CREATION & CLONING IN AZURE #
###################################

1 - Clone an entire VM
2 - Exit

Select the number of the task you want to do:
```
3. If you choose to exit, the program will close
```bash
###################################
# VMs CREATION & CLONING IN AZURE #
###################################

1 - Clone an entire VM
2 - Exit

Select the number of the task you want to do: 2
See you around!
```
4. If you continue with the cloning process, the program will ask you if you want to continue by using a VM Id, or not
```bash
##########################################################
# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ##
##########################################################


Do you know the ID of the VM to clone (y/n)?
```
5. If you write a `yes` answer, the program will ask you for the Id of the VM to be cloned. Just copy/paste or write your VM Id to proceed
```bash
#########################################################################
# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ## Using VM Id ##
#########################################################################


Please, enter the VM Id:
```
6. If you write a `no` answer, the program would load your available subscriptions first. You need to write the NUMBER of the subscription where the VM is. Then, the program would show you the resource groups in the selected subscription. Again, you need to write the NUMBER of the resource group in which your VM is. Finally, the VM names would be loaded and you need to write the NUMBER of the VM you want to clone
```bash
###########################################################################
# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ## Without VM Id ##
###########################################################################


        - Getting Subscriptions names...

A few accounts are skipped as they don't have 'Enabled' state. Use '--all' to display them.

1. SUB1                          2. SUB2

Please, enter the Subscription NUMBER of your VM to be cloned:
```
```bash
###########################################################################
# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ## Without VM Id ##
###########################################################################


        - Getting Resource Groups from the Subscription BCIRG3POCSUB...

1. RG1                          2. RG2

Please, enter the Resource Group NUMBER of your VM to be cloned:
```
```bash
###########################################################################
# VMs CREATION & CLONING IN AZURE ## Clone an entire VM ## Without VM Id ##
###########################################################################


        - Getting VMs from the Resource Group BCIRG3POC-RG-DPAVEZ001...

1. VM1                          2. VM2

Please, enter the VM NUMBER:
```
7. Just wait for the program to finish. You'll see status messages to know what the program is doing

## Need help?

If you have questions, you can contact me through my EMail: [daniel.pavez@usach.cl](mailto:daniel.pavez@usach.cl) or my LinkedIn profile [daniel-ips](www.linkedin.com/in/daniel-ips)