"""This is the 'nester.py'module,and it provides one function called
print_lol() which prints lists that may or may not include nested lists."""
'This comment is allowed either'
def print_lol(the_list,indent=False,level=0,place=sys.stdout):
    """"This function takes a positional argument called "the_list", which is any
Python list (of,possibly,nested lists).Each data item in the provided list 
is(recursively)printed to the screen on its own line.The argument "indent" indicate
that whether nested list enable indent,and argument "level" select the numbers of indent
TAB. The argument "place" the data where to write,default to the screen """
    for items in the_list:
        if isinstance(items,list):
            print_lol(items,indent,level+1,place)
        else:
            if indent == True:
                for tab_stop in range(level):
                    print("\t",end='',file=place)
            print(items,file=place)
