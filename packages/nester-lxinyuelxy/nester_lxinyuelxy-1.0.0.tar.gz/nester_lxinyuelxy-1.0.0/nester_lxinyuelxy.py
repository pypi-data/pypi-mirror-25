"""
This is a 'nester.py' module, which provide a function named print_lol(). The function of print_lol()
is printing a list included or not included a nester list.

"""
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
