from typing import Any
from importlib import import_module
from types import ModuleType
from typing import Union, List

# GH Actions
# nox
# TODO: build as standalone tool and as a package
# TODO: build abstraction for entity relationship checker 
# TODO: build abstraction for output format
# TODO: add documentation

class OOV:
    """main OOV class for generating object inspection.
    Currently the class only serves 1-2 objects.
    If there is one object, or the same object twice, given only self-cross-check will be performed.
    If there are two different objects given, the class will check both with them selves, and one again another.
    In the future the amount of objects will no be limited.
    """

    def __init__(self, obj: Union[str, ModuleType, List[Union[str, ModuleType]]]) -> None:
        # TODO: implement "noself: tuple[bool]" parameter to exlude matching objects within the same library
        self.parsed_objs: List[dict] = {}

        if isinstance(obj, str) or isinstance(obj, ModuleType):
            obj = [obj]
        elif not(isinstance(obj, list)):
            raise TypeError(
                "Parameter should be of type Union[str, ModuleType, List[Union[str, ModuleType]]], not: ",
                type(obj)
                )

        for e_obj in obj:
            if isinstance(e_obj, str):
                try:
                    self.parsed_objs[e_obj] = import_module(e_obj)
                except ModuleNotFoundError:
                    raise ModuleNotFoundError(e_obj, " not found.")
            elif isinstance(e_obj, ModuleType):
                try:
                    self.parsed_objs[e_obj.__name__] = e_obj
                except NameError:
                    raise NameError(
                        "Name ",
                        e_obj,
                        "not defined is current scope."
                        )
            else:
                raise TypeError(
                    "Parameter should be of type Union[str, ModuleType, List[Union[str, ModuleType]]], not: ",
                    type(e_obj)
                    )

    def _update_dict_inplace(
        self,
        d: dict,
        key1: str,
        key2: str,
        value: int
    ):
        """Store the results in a dictionary."""
        if key1 in d.keys():
            d[key1][key2] = value
        else:
            d[key1] = {}
            d[key1][key2] = value
        return

    def view_issubclass(self):
        """Generate results."""
        self.result: dict = {}
        job_list: list = []
        for i, e in enumerate(list(self.parsed_objs)):
            for w in list(self.parsed_objs)[i:]:
                job_list.append((e, w))
        for job in job_list:
            parsed_obj_1, parsed_obj_2 = job
            for elem_obj_1 in dir(self.parsed_objs[parsed_obj_1]):
                p_elem_obj_1: Any
                p_elem_obj_1 = eval(
                    "self.parsed_objs[parsed_obj_1]." + elem_obj_1
                    )
                for elem_obj_2 in dir(self.parsed_objs[parsed_obj_2]):
                    p_elem_obj_2: Any
                    p_elem_obj_2 = eval(
                        "self.parsed_objs[parsed_obj_2]." + elem_obj_2
                        )
                    try:
                        if issubclass(p_elem_obj_1, p_elem_obj_2):
                            self._update_dict_inplace(
                                self.result, elem_obj_1, elem_obj_2, 1
                                )
                        else:
                            self._update_dict_inplace(
                                self.result, elem_obj_1, elem_obj_2, 0
                                )
                    except TypeError:
                        # print("skipping: ", elem_obj_1, elem_obj_2)
                        pass
        return self.result
