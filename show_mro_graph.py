from collections     import abc
from collections.abc import *
import inspect
import graphviz

dot = graphviz.Digraph(comment='The Round Table')

def recurse_create(obj, dot):
    try:
        if obj[0][0].__name__ != 'object':
            print("create node: ", obj[0][0].__name__)
            dot.node(obj[0][0].__name__)
        else:
            pass
        
        if (len(obj[0][1])!=0) and (obj[0][0].__name__!='object') and (obj[0][1][0].__name__!='object'):
            print("create edge: ", obj[0][0].__name__, obj[0][1][0].__name__)
            dot.edge(obj[0][0].__name__, obj[0][1][0].__name__)
        
        r = recurse_create(obj[1], dot)
    
        return r
    
    except IndexError:
        return obj[0][0].__name__

def create_tree(obj: str, dot):
    cls_tree = inspect.getclasstree(inspect.getmro(eval(obj)))
    print("create node: ", obj)
    if obj != 'object':
        dot.node(obj)
    else:
        pass
    recurse_create(cls_tree, dot)
    return dot

for b in dir(__builtins__):
    try:
        create_tree(b, dot)
    except:
        pass

dot.render()