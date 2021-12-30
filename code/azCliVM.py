from azCliCaller import exAzCli

#VM cloner function
def createVM(vmData, vmSubId, clonedOSDiskId):
    print(f'\t- Getting data from the original VM and generating creation command...')
    nicsIds = vmData['networkProfile']['networkInterfaces']
    for nicsId in nicsIds:
        if str(nicsId['primary']) == 'None':
            nicId = nicsId['id']
    #gets the original VM NIC data
    nicData = exAzCli('network nic show --ids ' + nicId, False)
    createVMCommand = 'vm create -n ' + str(vmData['name']) + '-clone --subscription ' + vmSubId + ' -g ' + str(vmData['resourceGroup']) + ' -l ' + str(vmData['location']) + ' --attach-os-disk ' + clonedOSDiskId + ' --computer-name ' + str(vmData['name']) + '-clone --enable-agent true --nic-delete-option Delete' + ' --os-disk-delete-option ' + str(vmData['storageProfile']['osDisk']['deleteOption']) + ' --size ' + str(vmData['hardwareProfile']['vmSize'])
    if str(nicData['enableAcceleratedNetworking']) == 'None':
        createVMCommand = createVMCommand + ' --accelerated-networking false'
    else:
        createVMCommand = createVMCommand + ' --accelerated-networking true'
    if str(nicData['ipConfigurations'][0]['applicationSecurityGroups']) != 'None':
        createVMCommand = createVMCommand + ' --asgs ' + str(nicData['ipConfigurations'][0]['applicationSecurityGroups'])
    if str(vmData['identity']) != 'None':
        if str(vmData['identity']['userAssignedIdentities']) != 'None':
            createVMCommand = createVMCommand + ' --assign-identity ' + str(vmData['identity']['userAssignedIdentities'])
    if str(vmData['storageProfile']['osDisk']['osType']) == 'Linux':
        createVMCommand = createVMCommand + ' --os-type linux'
        if str(vmData['osProfile']) != 'None':
            if str(vmData['osProfile']['linuxConfiguration']['disablePasswordAuthentication']) != 'False':
                createVMCommand = createVMCommand + ' --patch-mode ' + str(vmData['osProfile']['linuxConfiguration']['patchSettings']['patchMode'])
            else:
                createVMCommand = createVMCommand + ' --patch-mode ' + str(vmData['osProfile']['linuxConfiguration']['patchSettings']['patchMode'])
    else:
        createVMCommand = createVMCommand + ' --os-type windows'
        if str(vmData['osProfile']) != 'None':
            createVMCommand = createVMCommand + ' --enable-auto-update ' + str(vmData['osProfile']['windowsConfiguration']['enableAutomaticUpdates']) + ' --patch-mode ' + str(vmData['osProfile']['windowsConfiguration']['patchSettings']['patchMode']) + ' --enable-hotpatching ' + str(vmData['osProfile']['windowsConfiguration']['patchSettings']['enableHotpatching'])
    if str(vmData['availabilitySet']) != 'None':
        createVMCommand = createVMCommand + ' --availability-set ' + str(vmData['availabilitySet'])
    if str(vmData['capacityReservation']) != 'None':
        createVMCommand = createVMCommand + ' --crg ' + str(vmData['capacityReservation'])
    if str(vmData['osProfile']) != 'None':
        if str(vmData['osProfile']['customData']) != 'None':
            createVMCommand = createVMCommand + ' --custom-data ' + str(vmData['osProfile']['customData'])
    if str(vmData['evictionPolicy']) != 'None':
        createVMCommand = createVMCommand + ' --eviction-policy ' + str(vmData['evictionPolicy'])
    if str(vmData['host']) != 'None':
        createVMCommand = createVMCommand + ' --host ' + str(vmData['host'])
    if str(vmData['hostGroup']) != 'None':
        createVMCommand = createVMCommand + ' --host-group ' + str(vmData['hostGroup'])
    if str(vmData['licenseType']) != 'None':
        createVMCommand = createVMCommand + ' --license-type ' + str(vmData['licenseType'])
    if str(nicData['networkSecurityGroup']) != 'None':
        createVMCommand = createVMCommand + ' --nsg ' + str(nicData['networkSecurityGroup'])
    if str(vmData['storageProfile']['osDisk']['managedDisk']['diskEncryptionSet']) != 'None':
        createVMCommand = createVMCommand + ' --os-disk-encryption-set ' + str(vmData['storageProfile']['osDisk']['managedDisk']['diskEncryptionSet'])
    if str(vmData['platformFaultDomain']) != 'None':
        createVMCommand = createVMCommand + ' --platform-fault-domain ' + str(vmData['platformFaultDomain'])
    if str(vmData['proximityPlacementGroup']) != 'None':
        createVMCommand = createVMCommand + ' --ppg ' + str(vmData['proximityPlacementGroup'])
    if str(vmData['priority']) != 'None':
        createVMCommand = createVMCommand + ' --priority ' + str(vmData['priority'])
    createVMCommand = createVMCommand + ' --subnet ' + str(nicData['ipConfigurations'][0]['subnet']['id'])
    if str(vmData['userData']) != 'None':
        createVMCommand = createVMCommand + ' --user-data ' + str(vmData['userData'])
    if str(vmData['zones']) != 'None':
        createVMCommand = createVMCommand + ' -z ' + str(vmData['zones'])
    
    print(f'\n\t\t- Creating the cloned VM (this could take a few minutes)...\n')
    #executes the VM-creation command
    newVM = exAzCli(createVMCommand, False)
    print(f'\t- Getting data from the cloned VM and cleaning if it applies...')
    #gets the cloned VM NIC id
    newVMData = exAzCli('vm show --ids ' + str(newVM['id']), False)
    newVMNicsIds = newVMData['networkProfile']['networkInterfaces']
    for newNicsId in newVMNicsIds:
        if str(newNicsId['primary']) == 'None':
            newNicId = newNicsId['id']
    #gets the cloned VM NIC id
    newNicData = exAzCli('network nic show --ids ' + newNicId, False)
    if str(nicData['networkSecurityGroup']) == 'None':
        print(f'\t\t- Deleting NSG from the cloned VM...')
        #detaches and deletes the NSG from the cloned VM
        exAzCli('network nic update --ids ' + newNicId + ' --remove networkSecurityGroup', False)
        exAzCli('network nsg delete --ids ' + str(newNicData['networkSecurityGroup']['id']), False)
    var = 0
    for ipConf in nicData['ipConfigurations']:
        if str(ipConf['publicIpAddress']) != 'None':
            var = 1
    if var == 0:
        for newIPConf in newNicData['ipConfigurations']:
            print(f'\t\t- Deleting public IP from the cloned VM...')
            #detaches and deletes the public IP from the cloned VM
            exAzCli('network nic ip-config update --ids ' + str(newIPConf['id']) + ' --remove PublicIpAddress', False)
            exAzCli('network public-ip delete --ids ' + str(newIPConf['publicIpAddress']['id']), False)
    return newVM