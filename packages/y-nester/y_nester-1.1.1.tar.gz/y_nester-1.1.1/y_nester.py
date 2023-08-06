"""This is the standard way to
   include a multiple-line comment in
   your code.
"""
import sys
def print_lol(the_list, indent=False, level=0, fn=sys.stdout):
    """This is suits"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1, fn)
        else:
            for tab_stop in range(level):
                print("\t", end="", file=fn)
            print(each_item, file=fn)