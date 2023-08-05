def print_lol(the_list,indent=0,level=0):
    """"print the list in nested """
    for i in the_list:
        if isinstance(i, list):
            level += 1
            print_lol(i,indent,level)
        else:
            if indent:
                for t in range(level):
                    print("\t",end='')
            print(i)
