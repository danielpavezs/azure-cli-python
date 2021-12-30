from azure.cli.core import get_default_cli
import os

def exAzCli(str,isString):
    if not isString:
        ipt = str.split()
    else:
        ipt = str.split('~')
    azc = get_default_cli()
    #calls CLI commands through the Python SDK
    azc.invoke(ipt, out_file = open(os.devnull, 'w'))
    #checks and returns the CLI answer
    if azc.result.result:
        return azc.result.result
    elif azc.result.error:
        return '{"return": "error"}'