"""This is the "nerster.py" module and it provides one function called print_lol() which prints lists that may or may not incluede nested lists."""
import sys
def print_lol(a_list, indent=False, level=0, fn=sys.stdout):
    """Prints each item in a list, recursively descending
       into nested lists (if necessary)."""

    for each_item in a_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fn)
        else:
            if indent:
                for l in range(level):
                    print("\t", end='', file=fn)
            print(each_item, file=fn)
