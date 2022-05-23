#!/usr/bin/env python3

import sys
import os
from datetime import datetime
from azure.cli.core import get_default_cli

def main(uN,uP,tI):
    exAzCli('login --service-principal -u ' + uN + ' -p ' + uP + ' --tenant ' + tI,False) #login to azure cli using service principal credentials
    subs = exAzCli('account list --all',False) #gets the subscriptions ids
    getSubnetsUDR(subs)

def getSubnetsUDR(subs):
    dir = 'tmp'
    pDir = '/tmp/'
    path = os.path.join(pDir,dir)
    try:
        os.stat(path)
    except:
        os.mkdir(path) #tries to create a directory to put the rollback shell script
    dtime = datetime.now().strftime("%Y%m%d%H%M")
    save_path = '/tmp/tmp'
    fnameRollback = '' + dtime + '_UDR_rollBack.sh'
    fFullName = os.path.join(save_path, fnameRollback)
    fRB = open(fFullName, 'w') #creates and opens the rollback file
    for sub in subs:
        subId = str(sub['id'])
        if str(sub['state']) == 'Enabled':
            print('Subscription → ' + str(sub['name']))
            vnetIds = exAzCli('network vnet list --subscription ' + subId + ' -o tsv --query [].id',False) #gets the vnets ids in subscription
            if str(vnetIds) != 'None':
                for vnetId in vnetIds:
                    vnetData = exAzCli('network vnet show --ids ' + vnetId + ' -o json',False) #gets the vnet data using its id
                    print('\tVNet → ' + vnetData['name'])
                    subnets = vnetData['subnets'] #getting subnets attribute from vnet
                    if str(subnets) != 'None':
                        for subnet in subnets:
                            print('\t\tSubnet → ' + str(subnet['name']))
                            subnetData = exAzCli('network vnet subnet show --ids ' + str(subnet['id']) + ' -o json',False) #getting subnet data
                            subnetUDR = subnetData['routeTable'] #getting route table attribute from subnet data
                            if str(subnetUDR) != 'None' and str(subnet['name']) != 'GatewaySubnet':
                                udrIdStr = str(subnetUDR['id']).split('/') #getting UDR id and split it by the '/' character
                                print('\t\t\tUDR in subnet → ' + str(subnetUDR['id']))
                                defaultRulesExistingUDR(subId,udrIdStr[4],str(vnetData['name']),udrIdStr[8],str(subnet['name']),str(vnetData['addressSpace']['addressPrefixes'][0]),str(subnetData['addressPrefix']),fRB) #calling the function that creates the default rules to an existing udr
                            elif str(subnetUDR) == 'None' and str(subnet['name']) != 'GatewaySubnet':
                                defaultRulesUDR(subId,str(subnet['resourceGroup']),str(vnetData['name']),str(subnet['name']),str(vnetData['addressSpace']['addressPrefixes'][0]),str(subnetData['addressPrefix']),fRB) #calling the function that creates an udr and its default rules
            privateEndpointsRulesUDR(subId,fRB) #calling the function that creates the private endpoints udr rules
    fRB.close()

def defaultRulesExistingUDR(subId,rgName,vnetName,udrName,subnetName,vNetAS,subnetAS,file):
    #adding the default rules to an existing udr
    print('\t\tAdding rules:')
    print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix 0.0.0.0/0 -n To_Azure_Firewall --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>')
    exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix 0.0.0.0/0 -n To_Azure_Firewall --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>',False)
    print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix <your hub vnet IP range> -n <your hub vnet name> --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>')
    exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix <your hub vnet IP range> -n <your hub vnet name> --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>',False)
    if vnetName != '<your hub vnet name>':
        print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix ' + vNetAS + ' -n ' + vnetName + ' --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>')
        exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix ' + vNetAS + ' -n ' + vnetName + ' --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>',False)
    print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix ' + subnetAS + ' -n ' + subnetName + ' --next-hop-type VnetLocal')
    exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' --address-prefix ' + subnetAS + ' -n ' + subnetName + ' --next-hop-type VnetLocal',False)
    #adds the rollback steps to the rollback bash file
    file.write('az network route-table route delete --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' -n To_Azure_Firewall\n')
    file.write('az network route-table route delete --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' -n <your hub vnet name>\n')
    file.write('az network route-table route delete --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' -n ' + vnetName + '\n')
    file.write('az network route-table route delete --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + udrName + ' -n ' + subnetName + '\n')

def defaultRulesUDR(subId,rgName,vnetName,subnetName,vNetAS,subnetAS,file):
    #creating an udr for the subnet
    print('\t\t\tCreating UDR  → ' + subnetName + '-UDR:')
    print('az network route-table create --subscription ' + subId + ' -g ' + rgName + ' -n ' + subnetName + '-UDR --disable-bgp-route-propagation true -l eastus2')
    exAzCli('network route-table create --subscription ' + subId + ' -g ' + rgName + ' -n ' + subnetName + '-UDR --disable-bgp-route-propagation true -l eastus2',False)
    #adding the default rules to the udr previously created
    print('\t\t\tAdding rules:')
    print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix 0.0.0.0/0 -n To_Azure_Firewall --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>')
    exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix 0.0.0.0/0 -n To_Azure_Firewall --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>',False)
    print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix <your hub vnet IP range> -n <your hub vnet name> --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>')
    exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix <your hub vnet IP range> -n <your hub vnet name> --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>',False)
    if vnetName != '<your hub vnet name>':
        print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix ' + vNetAS + ' -n ' + vnetName + ' --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>')
        exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix ' + vNetAS + ' -n ' + vnetName + ' --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>',False)
    print('az network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix ' + subnetAS + ' -n ' + subnetName + ' --next-hop-type VnetLocal')
    exAzCli('network route-table route create --subscription ' + subId + ' -g ' + rgName + ' --route-table-name ' + subnetName + '-UDR --address-prefix ' + subnetAS + ' -n ' + subnetName + ' --next-hop-type VnetLocal',False)
    #adding the urd to the subnet
    print('\t\t\tAdding UDR to the Subnet:')
    print('az network vnet subnet update --subscription ' + subId + ' -g ' + rgName + ' --vnet-name ' + vnetName + ' -n ' + subnetName + ' --route-table ' + subnetName + '-UDR\n')
    exAzCli('network vnet subnet update --subscription ' + subId + ' -g ' + rgName + ' --vnet-name ' + vnetName + ' -n ' + subnetName + ' --route-table ' + subnetName + '-UDR',False)
    #adds the rollback steps to the rollback bash file
    file.write('az network vnet subnet update --subscription ' + subId + ' -g ' + rgName + ' --vnet-name ' + vnetName + ' -n ' + subnetName + ' --remove routeTable\n')
    file.write('az network route-table delete --subscription ' + subId + ' -g ' + rgName + ' -n ' + subnetName + '-UDR\n')

def privateEndpointsRulesUDR(subId,file):
    rgs = exAzCli('group list --subscription ' + subId,False) #getting the subscription resource groups
    print('\nPE ROUTES')
    for rg in rgs:
        print('\tRG → ' + str(rg['name']))
        rgName = str(rg['name'])
        peIds = exAzCli('network private-endpoint list --subscription ' + subId + ' -g ' + rgName + ' --query [].id -o tsv',False) #checking if the resource group has a private endpoint
        if str(peIds) != 'None':
            for peId in peIds:
                peData = exAzCli('network private-endpoint show --ids ' + peId,False) #getting the private endpoint id
                subnetIdStr = str(peData['subnet']['id']).split('/') #splitting the private endpoint id by '/'
                print('\t\tPE → ' + str(peData['name']) + ' in subnet → ' + subnetIdStr[10])
                print('\t\t\tVnet subnets → ' + subnetIdStr[8])
                vnetData = exAzCli('network vnet subnet list --subscription ' + subId + ' -g ' + subnetIdStr[4] + ' --vnet-name ' + subnetIdStr[8],False) #getting the subnets from the private endpoint vnet
                if str(vnetData) != 'None':
                    for subnetData in vnetData:
                        if str(subnetData['routeTable']) != 'None':
                            subnetUDRStr = str(subnetData['routeTable']['id']).split('/') #getting the udr id from the subnet
                            peNics = peData['networkInterfaces']
                            if str(peNics) != 'None':
                                for peNic in peNics:
                                    nicData = exAzCli('network nic show --ids ' + str(peNic['id']),False) #getting the private endpoint network interface
                                    nicIPs = nicData['ipConfigurations']
                                    for nicIP in nicIPs:
                                        if str(subnetData['name']) != subnetIdStr[10]:
                                            #adding private endpoint rule to a subnet
                                            print('az network route-table route create --subscription ' + subId + ' -g ' + subnetUDRStr[4] + ' --route-table-name ' + subnetUDRStr[8] + ' --address-prefix ' + str(nicIP['privateIpAddress']) + '/32 -n ' + str(peData['name']) + ' --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>')
                                            exAzCli('network route-table route create --subscription ' + subId + ' -g ' + subnetUDRStr[4] + ' --route-table-name ' + subnetUDRStr[8] + ' --address-prefix ' + str(nicIP['privateIpAddress']) + '/32 -n ' + str(peData['name']) + ' --next-hop-type VirtualAppliance --next-hop-ip-address <your Azure Firewal private IP>',False)
                                            #adds the rollback step to the rollback bash file
                                            file.write('az network route-table route delete --subscription ' + subId + ' -g ' + subnetUDRStr[4] + ' --route-table-name ' + subnetUDRStr[8] + ' -n ' + str(peData['name']) + '\n')
                                        else:
                                            print('\t\t\t\tSubnet → ' + str(subnetData['name']) + ' do nothing to ' + subnetUDRStr[8])

def exAzCli(str,isString):
    if not isString:
        ipt = str.split()
    else:
        ipt = str.split('~')
    azc = get_default_cli()
    azc.invoke(ipt, out_file = open(os.devnull, 'w')) #executes the Azure CLI command
    if azc.result.result:
        return azc.result.result
    elif azc.result.error:
        return '{"return": "error"}'

if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise Exception('Requires three arguments: 1: Service Principal id, 2: Service Principal password and Tenant id')
    main(sys.argv[1],sys.argv[2],sys.argv[3])