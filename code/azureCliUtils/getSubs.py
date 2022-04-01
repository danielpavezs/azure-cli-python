#!/usr/bin/env python3

import sys
import os
from azure.cli.core import get_default_cli

def main(uN,uP,tI):
    commnd = f'login --service-principal -u {uN} -p {uP} --tenant {tI}'
    exAzCli(commnd, False) #login to azure cli using service principal credentials
    subs = exAzCli('account list --all', False) #executing cli command
    showingSubs(subs)

def exAzCli(str,isString):
    if not isString:
        ipt = str.split()
    else:
        ipt = str.split('~')
    azc = get_default_cli()
    azc.invoke(ipt, out_file = open(os.devnull, 'w'))
    if azc.result.result:
        return azc.result.result
    elif azc.result.error:
        return '{"return": "error"}'

def showingSubs(subs):
    for sub in subs:
        print('Subscription "' + str(sub['name']) + '" is currently ' + str(sub['state']) + ' and has the Id: ' + str(sub['id']))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise Exception('Requires three arguments: 1: Service Principal id, 2: Service Principal password and Tenant id')
    main(sys.argv[1],sys.argv[2],sys.argv[3])
