"""Demo function to create distribution"""
def printList(inputList):
    for each_item in inputList:
        if (isinstance(each_item,list)):
            printList(each_item)
        else:
            print(each_item)
