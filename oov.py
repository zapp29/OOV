from pandas import DataFrame
from typing import Any
from importlib import import_module

# TODO: add tests
# TODO: build as standalone tool and as a package
# TODO: build abstraction for entity relationship checker 
# TODO: build abstraction for output format

class OOV:
    """main OOV class for generating object inspection.
    """

    def __init__(self, 
                obj: list[Any], 
                imp: list[bool] = (True,True)
        ) -> None:
        self.obj_names:   list[str]  = obj
        self.parsed_objs: list[dict] = {}
        
        if len(obj) != len(imp):
            # TODO implement proper Exception; how to create exception that will print proper error message
            raise Exception

        for e_obj,e_imp in list(zip(obj,imp)):
            if e_imp:
                try:
                    self.parsed_objs[e_obj] = import_module(e_obj)
                except:
                    print("ModuleNotFoundError: ", e_obj, " not found.")
            else:
                try:
                    self.parsed_objs[e_obj] = eval(e_obj)
                except NameError:
                    print("Name ", e_obj, "not defined is current scope.")    
    
    def _update_dict_inplace(self, 
                    d: dict, 
                    key1: str, 
                    key2: str, 
                    value: int):
        """private function for storing the results in a self.result dictionary"""
        if key1 in d.keys():
            d[key1][key2] = value
        else:
            d[key1] = {}
            d[key1][key2] = value
        return
    
    def view_issubclass(self):
        """function to generate results"""
        # TODO: redo function to use new model from __init__
        self.result: dict = {}
        for elem_obj_1 in dir(self.parsed_obj_1[self.obj_1_name]): 
            p_elem_obj_1: Any = eval("self.parsed_obj_1[self.obj_1_name]." + elem_obj_1)
            for elem_obj_2 in dir(self.parsed_obj_2[self.obj_2_name]):
                p_elem_obj_2: Any = eval("self.parsed_obj_2[self.obj_2_name]." + elem_obj_2)
                try:
                    if issubclass(p_elem_obj_1, p_elem_obj_2):
                        self._update_dict_inplace(self.result, elem_obj_1, elem_obj_2, 1)
                    else:
                        self._update_dict_inplace(self.result, elem_obj_1, elem_obj_2, 0)
                except TypeError:
                    print("skipping: ", elem_obj_1, elem_obj_2)
        return self.result

tmp = OOV(("collections.abc","collections.abc"),(True,True)).view_issubclass()

print(DataFrame.from_dict(tmp))