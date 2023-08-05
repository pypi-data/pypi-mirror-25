"""This is the standard way to
   include a multiple-line comment in
   your code.
"""
def print_lol(the_list):
    """This is suits"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)