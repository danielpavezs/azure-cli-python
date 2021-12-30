from azCliCaller import exAzCli

#the function that creates an O.S. disk
def createOSDisk(osDiskId, vmName, dSubId, RGName):
    print(f'\t- Getting data from the original disk and generating creation command...')
    #gets the O.S-disk data to create a proper disk-creation command
    osDiskData = exAzCli('disk show --ids ' + osDiskId, False)
    createDiskCommand = 'disk create -n ' + vmName + '-OsDisk-clone --subscription ' + dSubId + ' -g ' + RGName + ' -l ' + str(osDiskData['location']) + ' -z ' + str(osDiskData['diskSizeGb']) + ' --network-access-policy ' + str(osDiskData['networkAccessPolicy']) + ' --os-type ' + str(osDiskData['osType']) + ' --public-network-access ' + str(osDiskData['publicNetworkAccess']) + ' --sku ' + str(osDiskData['sku']['name']) + ' --source ' + str(osDiskId)
    if str(osDiskData['hyperVGeneration']) != 'None':
        createDiskCommand = createDiskCommand + ' --hyper-v-generation ' + str(osDiskData['hyperVGeneration'])
    if str(osDiskData['supportedCapabilities']['acceleratedNetwork']) == 'None':
        createDiskCommand = createDiskCommand + ' --accelerated-network false'
    else:
        createDiskCommand = createDiskCommand + ' --accelerated-network true'
    if str(osDiskData['burstingEnabled']) == 'None':
        createDiskCommand = createDiskCommand + ' --enable-bursting false'
    else:
        createDiskCommand = createDiskCommand + ' --enable-bursting true'
    if str(osDiskData['supportsHibernation']) != 'None':
        createDiskCommand = createDiskCommand + ' --support-hibernation true'
    if str(osDiskData['zones']) != 'None':
        createDiskCommand = createDiskCommand + ' --zone ' + str(osDiskData['zones'])
    if str(osDiskData['diskAccessId']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-access ' + str(osDiskData['diskAccessId'])
    if str(osDiskData['encryption']['diskEncryptionSetId']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-encryption-set ' + str(osDiskData['encryption']['diskEncryptionSetId'])
    if str(osDiskData['diskIopsReadOnly']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-iops-read-only ' + str(osDiskData['diskIopsReadOnly'])
    if str(osDiskData['diskIopsReadWrite']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-iops-read-write ' + str(osDiskData['diskIopsReadWrite'])
    if str(osDiskData['diskMBpsReadOnly']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-mbps-read-only ' + str(osDiskData['diskMBpsReadOnly'])
    if str(osDiskData['diskMBpsReadWrite']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-mbps-read-write ' + str(osDiskData['diskMBpsReadWrite'])
    if str(osDiskData['encryption']['type']) != 'None':
        createDiskCommand = createDiskCommand + ' --encryption-type ' + str(osDiskData['encryption']['type'])
    if str(osDiskData['creationData']['logicalSectorSize']) != 'None':
        createDiskCommand = createDiskCommand + ' --logical-sector-size ' + str(osDiskData['creationData']['logicalSectorSize'])
    if str(osDiskData['maxShares']) != 'None':
        createDiskCommand = createDiskCommand + ' --max-shares ' + str(osDiskData['maxShares'])
    if str(osDiskData['tier']) != 'None':
        createDiskCommand = createDiskCommand + ' --tier ' + str(osDiskData['tier'])
    if str(osDiskData['creationData']['uploadSizeBytes']) != 'None':
        createDiskCommand = createDiskCommand + ' --upload-size-bytes ' + str(osDiskData['creationData']['uploadSizeBytes'])
    print(f'\t\t- Creating the cloned OS disk...')
    #calls the disk-creation command
    clonedOSDisk = exAzCli(createDiskCommand, False)
    return clonedOSDisk

#the function that creates a data disk
def createDisk(diskId, diskName, dSubId, RGName):
    print(f'\t- Getting data from the original disk and generating creation command...')
    #gets the data-disk data to create a proper disk-creation command
    diskData = exAzCli('disk show --ids ' + diskId, False)
    createDiskCommand = 'disk create -n ' + diskName + '-clone --subscription ' + dSubId + ' -g ' + RGName + ' -l ' + str(diskData['location']) + ' -z ' + str(diskData['diskSizeGb']) + ' --network-access-policy ' + str(diskData['networkAccessPolicy']) + ' --public-network-access ' + str(diskData['publicNetworkAccess']) + ' --sku ' + str(diskData['sku']['name']) + ' --source ' + str(diskId)
    if str(diskData['hyperVGeneration']) != 'None':
        createDiskCommand = createDiskCommand + ' --hyper-v-generation ' + str(diskData['hyperVGeneration'])
    if str(diskData['supportedCapabilities']) != 'None':
        if str(diskData['supportedCapabilities']['acceleratedNetwork']) == 'None':
            createDiskCommand = createDiskCommand + ' --accelerated-network false'
        else:
            createDiskCommand = createDiskCommand + ' --accelerated-network true'
    if str(diskData['burstingEnabled']) == 'None':
        createDiskCommand = createDiskCommand + ' --enable-bursting false'
    else:
        createDiskCommand = createDiskCommand + ' --enable-bursting true'
    if str(diskData['supportsHibernation']) != 'None':
        createDiskCommand = createDiskCommand + ' --support-hibernation true'
    if str(diskData['zones']) != 'None':
        createDiskCommand = createDiskCommand + ' --zone ' + str(diskData['zones'])
    if str(diskData['diskAccessId']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-access ' + str(diskData['diskAccessId'])
    if str(diskData['encryption']['diskEncryptionSetId']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-encryption-set ' + str(diskData['encryption']['diskEncryptionSetId'])
    if str(diskData['diskIopsReadOnly']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-iops-read-only ' + str(diskData['diskIopsReadOnly'])
    if str(diskData['diskIopsReadWrite']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-iops-read-write ' + str(diskData['diskIopsReadWrite'])
    if str(diskData['diskMBpsReadOnly']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-mbps-read-only ' + str(diskData['diskMBpsReadOnly'])
    if str(diskData['diskMBpsReadWrite']) != 'None':
        createDiskCommand = createDiskCommand + ' --disk-mbps-read-write ' + str(diskData['diskMBpsReadWrite'])
    if str(diskData['encryption']['type']) != 'None':
        createDiskCommand = createDiskCommand + ' --encryption-type ' + str(diskData['encryption']['type'])
    if str(diskData['creationData']['logicalSectorSize']) != 'None':
        createDiskCommand = createDiskCommand + ' --logical-sector-size ' + str(diskData['creationData']['logicalSectorSize'])
    if str(diskData['maxShares']) != 'None':
        createDiskCommand = createDiskCommand + ' --max-shares ' + str(diskData['maxShares'])
    if str(diskData['tier']) != 'None':
        createDiskCommand = createDiskCommand + ' --tier ' + str(diskData['tier'])
    if str(diskData['creationData']['uploadSizeBytes']) != 'None':
        createDiskCommand = createDiskCommand + ' --upload-size-bytes ' + str(diskData['creationData']['uploadSizeBytes'])
    print(f'\t\t- Creating the cloned disk from {diskName}...')
    #calls the disk-creation command
    clonedOSDisk = exAzCli(createDiskCommand, False)
    return clonedOSDisk

#the function that attaches a disk to a VM
def attachDisk(vmId, diskId):
    vmIdArr = str(vmId).split('/')
    diskIdArr = str(diskId).split('/')
    print(f'\t\t- Attaching disk {diskIdArr[8]} to VM {vmIdArr[8]}...')
    #calls the disk-attachment command
    attachment = exAzCli('vm disk attach --subscription ' + vmIdArr[2] + ' -g ' + vmIdArr[4] + ' --vm-name ' + vmIdArr[8] + ' --ids ' + str(diskId), False)
    return attachment