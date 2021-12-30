from azCliCaller import exAzCli

#creates a command that allows us to create a command to copy tags
def addTags(commandToGetTags, resourceId2):
    #gets the original resource's tags
    originalTags = exAzCli(commandToGetTags, False)
    print(f'\t- Getting tags from the original resource...')
    if str(originalTags) != 'None':
        #creates the command adding the tags one by one
        addTagsCommand = 'tag~update~--resource-id~' + resourceId2 + '~--operation~merge~--tags~'
        for tag in originalTags:
            addTagsCommand = addTagsCommand + str(tag) + '=' + str(originalTags[tag]) + '~'
    return addTagsCommand