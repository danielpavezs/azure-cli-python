#!/usr/bin/env python3

import os
from azure.cli.core import get_default_cli
from datetime import datetime

def main(uN,uP,tI,sA,sAK,sub):
    logIn(uN,uP,tI)
    getPubOff(sA,sAK,sub)

def getPubOff(sA,sAK,sb):
    fname = datetime.now().strftime("%Y%m%d%H%M") + 'publisherOffers.csv' #creates a file to save the data
    f = open(fname, 'w')
    f.write('Publisher,Offer,Image URN\n')
    pubs = exAzCli('vm image list-publishers -l eastus2 -o json --query [].name', False) #gets a list of available Publishers
    for pub in pubs:
        offs = exAzCli('vm image list-offers -l eastus2 -p ' + pub + ' -o json --query [].name', False) #for every Publisher, gets a list of available Offers
        if str(offs) != 'None':
            for off in offs:
                imgs = exAzCli('vm image list -f ' + off + ' --all -o json', False) #for every Publisher and Offer, gets a list of available VM images
                if str(imgs) != 'None':
                    for img in imgs:
                        f.write(str(pub) + ',' + str(off) + ',' + str(img['urn']) + '\n')
    f.close()
    uploadFile('report/pubOff',os.getcwd() + '/' + fname,sAK,sA,sb)

def uploadFile(c,file,sAK,sA,sub):
    exAzCli('storage blob upload -c ' + c + ' -f ' + file + ' --account-key ' + sAK + ' --account-name ' + sA + ' --auth-mode key --subscription ' + sub, False) #uploads the file to a Storage Account using the Account Key

def logIn(uN,uP,tI):
    commnd = f'login --service-principal -u {uN} -p {uP} --tenant {tI}'
    exAzCli(commnd, False) #Logs in to the platform using the given credentials

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
        raise Exception('Requires three arguments: 1: Service Principal id, 2: Service Principal password, 3: Tenant id, 4: Storage Account Name, 5: Storage Account Key and Storage Account Subscription')
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
