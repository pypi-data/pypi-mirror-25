"""this is "nester.py" module and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""

def print_lol(the_list):
    """this
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(the_list)
        else:
            print(each_item)

