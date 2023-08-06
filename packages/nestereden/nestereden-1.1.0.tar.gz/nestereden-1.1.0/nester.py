''' 这是“wester.py”模块，提供了一个名为print_lol的函数
    这个函数的作用是打印列表，
    其中有可能包含（也可能不包含）嵌套列表。'''

''' 这个函数取一个位置参数名为“theList”这可以是任何python列表
    也可以使包含嵌套的列表。所指定的列表中的每个数据项会（递归地）
    输出到屏幕上，各数据项各占一行。'''
def print_lol(theList,indent=False,level=0):
    for eachItem in theList:
        if isinstance(eachItem,list):
            print_lol(eachItem,indent,level+1)
        else:
            if indent:
                for tabStop in range(level):
                    print("\t",end='')
            print(eachItem)
