'''this is nester.py module, give a function named print_lol(), 
 it is used to print element of a list'''

def print_lol(the_list,level):
    '''first parameter the_list should be a list, will be print recursively'''
    '''second parameter level indicates inserting tab while a list is nested'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
