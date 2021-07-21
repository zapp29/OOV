from pandas import DataFrame
from typing import Any
from importlib import import_module

# TODO: add tests
# TODO: build as standalone tool and as a package
# TODO: create documentation: Sphinx
# TODO: build abstraction for entity relationship checker 
# TODO: build abstraction for output format

class OOV:
    """main OOV class for generating object inspection.
    """

    def __init__(self, 
                obj: tuple[Any,Any], 
                imp: tuple[bool,bool] = (True,True)
        ):
        self.obj_1_name: str = obj[0]
        self.obj_2_name: str = obj[1]
        self.parsed_obj_1: dict = {}
        self.parsed_obj_2: dict = {}
        imp = tuple(imp)
        if imp[0]:
            try:
                self.parsed_obj_1[self.obj_1_name] = import_module(self.obj_1_name)
            except ModuleNotFoundError:
                print("ModuleNotFoundError: ", self.obj_1_name, " not found.")
        else:
            try:
                self.parsed_obj_1[self.obj_1_name] = eval(self.obj_1_name)
            except NameError:
                print("Name ", self.obj_1_name, "not defined is current scope.")
        if imp[1]:
            try:
                self.parsed_obj_2[self.obj_2_name] = import_module(self.obj_2_name)
            except ModuleNotFoundError:
                print("ModuleNotFoundError: ", self.obj_2_name, " not found.")
        else:
            try:
                self.parsed_obj_2[self.obj_2_name] = eval(self.obj_2_name)
            except NameError:
                print("Name ", self.obj_2_name, "not defined is current scope.")
    
    def _update_dict(self, d, key1, key2, value):
        if key1 in d.keys():
            d[key1][key2] = value
        else:
            d[key1] = {}
            d[key1][key2] = value
        return
    
    def view_issubclass(self):
        """function to generate results"""
        self.result = {}
        for elem_obj_1 in dir(self.parsed_obj_1[self.obj_1_name]):
            p_elem_obj_1 = eval("self.parsed_obj_1[self.obj_1_name]." + elem_obj_1)
            for elem_obj_2 in dir(self.parsed_obj_2[self.obj_2_name]):
                p_elem_obj_2 = eval("self.parsed_obj_2[self.obj_2_name]." + elem_obj_2)
                try:
                    if issubclass(p_elem_obj_1, p_elem_obj_2):
                        self._update_dict(self.result, elem_obj_1, elem_obj_2, 1)
                    else:
                        self._update_dict(self.result, elem_obj_1, elem_obj_2, 0)
                except TypeError:
                    print("skipping: ", elem_obj_1, elem_obj_2)
        return self.result

#tmp = OOV(("collections.abc","collections.abc"),(True,True)).view_issubclass()

#print(DataFrame.from_dict(tmp))