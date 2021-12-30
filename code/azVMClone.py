from azCliCaller import exAzCli
from azCliDisk import createOSDisk, createDisk, attachDisk
from azCliTag import addTags
from azCliVM import createVM
from printMessage import printHead

#the following functions controls the clone functionality
def idOrNot():
    printHead(2)
    #validates if the user wants to clone a VM by searching it, or using the VMs Id
    opt = input('\nDo you know the ID of the VM to clone (y/n)? ').lower().replace(' ', '')
    while True:
        if opt == 'y' or opt == 'yes':
            printHead(3)
            vmId = input('\nPlease, enter the VM Id: ')
            cloneWithID(vmId)
            break
        elif opt == 'n' or opt == 'no':
            cloneBySearch()
            break
        else:
            opt = input('\nInvalid option, please try again (y/n)? ').lower().replace(' ', '')


def cloneWithID(vmIdInput):
    printHead(3)
    vmId = vmIdInput
    while True:
        print(f'\n\t- Getting data from the original VM...')
        #gets the original VM data using the Id
        vmData = exAzCli('vm show --ids ' + vmId, False)
        if str(vmData) != '{"return": "error"}':
            osDiskId = vmData['storageProfile']['osDisk']['managedDisk']['id']
            osDiskIdArr = osDiskId.split('/')
            vmIdArr = str(vmData['id']).split('/')
            #calls the function that clones the OS disk
            clonedOSDisk = createOSDisk(osDiskId, vmData['name'], osDiskIdArr[2], osDiskIdArr[4])
            #adds the original tags to the cloned OS disk
            addTagsCommand = addTags('disk show --ids ' + osDiskId + ' --query "tags"', clonedOSDisk['id'])
            print(f'\t\t- Adding tags from the original to the cloned OS disk...')
            exAzCli(addTagsCommand, True)
            #calls the function that clones VM using the cloned OS disk
            newVMData = createVM(vmData, vmIdArr[2], clonedOSDisk['id'])
            #adds the original tags to the cloned VM
            addTagsCommand = addTags('vm show --ids ' + str(vmData['id']) + ' --query "tags"', newVMData['id'])
            print(f'\t\t- Adding tags from the original the cloned VM...')
            exAzCli(addTagsCommand, True)
            #uses a loop to get all the original data disks to clone/attach them to new VM one by one
            if str(vmData['storageProfile']['dataDisks']) != 'None':
                for dataDiskData in vmData['storageProfile']['dataDisks']:
                    diskId = dataDiskData['managedDisk']['id']
                    diskIdArr = diskId.split('/')
                    #if exists, clones a data disk
                    clonedDisk = createDisk(diskId, dataDiskData['name'], diskIdArr[2], diskIdArr[4])
                    #adds the original tags to the cloned data disk
                    addTagsCommand = addTags('disk show --ids ' + diskId + ' --query "tags"', clonedDisk['id'])
                    print(f'\t\t- Adding tags from the original to the cloned OS disk...')
                    exAzCli(addTagsCommand, True)
                    #attaches the data disk to the cloned VM
                    attachDisk(newVMData['id'], clonedDisk['id'])
            newVMDataIdArr = str(newVMData['id']).split('/')
            print(f'\n\nThe cloned Virtual Machine {newVMDataIdArr[8]} has been created!\n\n')
            break
        else:
            printHead(3)
            vmId = input('\nInvalid VM Id, please try again please: ')

#the function will navigate through the Tenant subscriptions, resource groups and VMs to select a proper VM Id
def cloneBySearch():
    printHead(4)
    print(f'\t- Getting Subscriptions names...\n')
    #gets the available subscriptions
    subs = exAzCli('account list', False)
    count = 1
    print('\n', end="")
    for sub in subs:
        subName = str(sub['name'])
        print(f'{count}. {subName}\t\t\t\t', end="")
        if count%3 == 0:
            print('\n', end="")
        sub['cloudName'] = str(count)
        count+=1
    selectedSub = input('\n\nPlease, enter the Subscription NUMBER of your VM to be cloned: ')
    while True:
        if 1 <= int(selectedSub) <= count-1:
            subName = subs[int(selectedSub)-1]['name']
            printHead(4)
            print(f'\t- Getting Resource Groups from the Subscription {subName}...\n')
            #using the subscriptions selected by the user gets the resource groups
            rgs = exAzCli('group list --subscription ' + subs[int(selectedSub)-1]['id'], False)
            count = 1
            for rg in rgs:
                rgName = str(rg['name'])
                print(f'{count}. {rgName}\t\t\t\t\t', end="")
                if count%2 == 0:
                    print('\n', end="")
                sub['managedBy'] = str(count)
                count+=1
            selectedRG = input('\n\nPlease, enter the Resource Group NUMBER of your VM to be cloned: ')
            while True:
                if 1 <= int(selectedRG) <= count-1:
                    rgName = str(rgs[int(selectedRG)-1]['name'])
                    printHead(4)
                    print(f'\t- Getting VMs from the Resource Group {rgName}...\n')
                    #gets the VMs inside the selected resource group
                    vms = exAzCli('vm list --subscription ' + subs[int(selectedSub)-1]['id'] + ' -g ' + rgName, False)
                    count = 1
                    for vm in vms:
                        vmName = str(vm['name'])
                        print(f'{count}. {vmName}\t\t\t\t\t', end="")
                        if count%2 == 0:
                            print('\n', end="")
                        count+=1
                    selectedVM = input('\n\nPlease, enter the VM NUMBER: ')
                    while True:
                        if 1 <= int(selectedVM) <= count-1:
                            selectedVMId = str(vms[int(selectedVM)-1]['id'])
                            #using the selected VM id calls the function that clones using an Id
                            cloneWithID(selectedVMId)
                            break
                        else:
                            selectedVM = input('\nInvalid VM NUMBER, please try again: ')
                    break
                else:
                    selectedRG = input('\nInvalid Resource Group NUMBER, please try again: ')
            break
        else:
            selectedSub = input('\nInvalid Subscription NUMBER, please try again: ')