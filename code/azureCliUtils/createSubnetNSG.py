#!/usr/bin/env python3

import sys
import os
from datetime import datetime
from azure.cli.core import get_default_cli

def main(uN,uP,tI):
    lng = f'login --service-principal -u {uN} -p {uP} --tenant {tI}'
    exAzCli(lng,False) #login to azure cli using service principal credentials
    subs = exAzCli('account list --all',False) #gets subscription data
    showingVNetRGs(subs)

def showingVNetRGs(subs):
    for sub in subs:
        subId = str(sub['id'])
        getVnetIds = f'network vnet list --subscription {subId} -o tsv --query [].id'
        vnetIds = exAzCli(getVnetIds,False) #gets virtual networks data
        if str(vnetIds) != 'None':
            for vnetId in vnetIds:
                getVnetRG = f'network vnet show --ids {vnetId} -o tsv --query resourceGroup'
                vnetRG = exAzCli(getVnetRG,False) #gets virtual network resource group data
                getSubnets = f'network vnet show --ids {vnetId} -o tsv --query subnets'
                subnets = exAzCli(getSubnets,False) #gets virtual network subnets data
                if str(subnets) != 'None':
                    for subnet in subnets:
                        subnetId = str(subnet['id'])
                        subnetName = str(subnet['name'])
                        getSubnetNSG = f'network vnet subnet show --ids {subnetId} -o json --query networkSecurityGroup'
                        subnetNSG = exAzCli(getSubnetNSG,False) #gets subnet network security group data
                        if str(subnetNSG) == 'None' and subnetName != 'GatewaySubnet':
                            addNSG(subId,vnetRG,subnetName,subnetId)
                            msg = f'{datetime.now().strftime("%Y.%m.%d %H:%M:%S")}: Subnet \"{subnetName}\" without NSG.\n\tVirtual Network: {vnetId}\n\tNSG \"{subnetName}-NSG\" added to Subnet\n'
                            print(msg)

def addNSG(subId,vnetRG,subnetName,subnetId):
    createNSG = f'network nsg create --subscription {subId} -g {vnetRG} -l eastus2 -n {subnetName}-NSG'
    nsgData = exAzCli(createNSG,False) #creates the network security group
    nsgId = str(nsgData['NewNSG']['id'])
    addRuleNSG = f'network~nsg~rule~create~--subscription~{subId}~-g~{vnetRG}~--nsg-name~{subnetName}-NSG~-n~AllowAllInbound~--priority~100~--access~Allow~--description~"Temporal rule: allow all inbound"~--destination-address-prefixes~*~--destination-port-ranges~*~--direction~Inbound~--protocol~*~--source-address-prefixes~*'
    exAzCli(addRuleNSG,True) #adds an "allow inbound" default rule to the network security group
    addRuleNSG = f'network~nsg~rule~create~--subscription~{subId}~-g~{vnetRG}~--nsg-name~{subnetName}-NSG~-n~AllowAllOutbound~--priority~100~--access~Allow~--description~"Temporal rule: allow all outbound"~--destination-address-prefixes~*~--destination-port-ranges~*~--direction~Outbound~--protocol~*~--source-address-prefixes~*'
    exAzCli(addRuleNSG,True) #adds an "allow outbound" default rule to the network security group
    attachNSG = f'network vnet subnet update --ids {subnetId} --nsg {nsgId}' #attaches the network security group to a Subnet
    exAzCli(attachNSG,False) #attaches the new network security group to the subnet

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