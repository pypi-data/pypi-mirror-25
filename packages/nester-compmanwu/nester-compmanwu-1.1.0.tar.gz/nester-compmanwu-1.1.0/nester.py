def print_lol2(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol2(each_item,level+1)
        else:
            for tab_stop in range(level):
                 print("\t",end=' ')
            print(each_item)
                
