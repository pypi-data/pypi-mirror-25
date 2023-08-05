'''this is nester.py module, give a function named print_lol(), 
 it is used to print element of a list'''

def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)