"""这是"nester.py"模块，提供了一个名为print_lol()的函数，这个函数的作用是打印列表
    ，其中有可能包括（也可能不包含）嵌套列表"""
def print_lol(the_list,indent = False,level = 0):
    """这个函数取一个位置参数，名为“the_list”,这可以是任何python列表（也可以是
        包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归的）输出到屏幕上，
        各个数据项占一行"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t"*level,end=' ')
            print(each_item)