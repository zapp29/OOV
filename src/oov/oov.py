"""Define main OOV class."""
from importlib import import_module
from types import ModuleType
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

# TODO: build abstraction for entity relationship checker
# TODO: build abstraction for output format
# TODO: build abstraction for presentation format
# TODO: add documentation
# TODO: work with packages that are not installed


class Observation:
    """Pass."""

    def __init__(self, data, metadata) -> None:
        """Initialize internal objects.

        Args:
            data: blabla
            metadata: blabla
        """
        self._data = data
        self._metadata = metadata

    def get_data(self):
        """Pass."""
        return self._data

    def get_metadata(self, format=dict):
        """Pass."""
        if format == dict:
            return self._metadata
        if format == list:
            result = []
            for key1 in self._metadata.keys():
                for key2 in self._metadata[key1]:
                    result.append([self._metadata[key1][key2], key1, key2])
            return result


class OOV:
    """Main OOV class for generating object inspection.

    Currently the class only serves 1-2 objects.

    If there is one object, or the same object twice,
    given only self-cross-check will be performed.

    If there are two different objects given,
    the class will check both with them selves, and one again another.

    In the future the amount of objects will not be limited.
    """

    def __init__(
        self,
        obj: Union[
            str, ModuleType, List[str], List[ModuleType], List[Union[str, ModuleType]]
        ],
    ) -> None:
        """Initialize internal objects.

        Args:
            obj: blabla

        Raises:
            ModuleNotFoundError: blabla
            TypeError: blabla
        """
        # TODO: implement "noself: tuple[bool]"
        # parameter to exlude matching objects within the same library
        self.parsed_objs: Dict[str, ModuleType] = {}
        self._counter: int = 1

        if isinstance(obj, str) or isinstance(obj, ModuleType):
            obj = [obj]
        elif not (isinstance(obj, list)):
            raise TypeError(
                "Parameter should be of type "
                "Union[str, ModuleType, List[Union[str, ModuleType]]], not: ",
                type(obj),
            )

        for e_obj in obj:
            if isinstance(e_obj, str):
                try:
                    self.parsed_objs[e_obj] = import_module(e_obj)
                except ModuleNotFoundError:
                    raise ModuleNotFoundError(e_obj, " not found.")
            elif isinstance(e_obj, ModuleType):
                self.parsed_objs[e_obj.__name__] = e_obj

            else:
                raise TypeError(
                    "Parameter should be of type "
                    "Union[str, ModuleType, List[Union[str, ModuleType]]], not: ",
                    type(e_obj),
                )

    def _update_dict_inplace(
        self, d: Dict[str, Dict[str, Any]], key1: str, key2: str, value: int
    ) -> None:
        """Store the results in a dictionary."""
        if key1 in d.keys():
            d[key1][key2] = value
        else:
            d[key1] = {}
            d[key1][key2] = value
        return

    def _update_enumerated_dict(
        self, d: Dict[str, Dict[str, int]], key1: str, key2: str
    ) -> None:
        """Store the results in a dictionary.

        if d[key1][key2] exists:
            do nothing
        if d[key1][key2] doesn't exits:
            d[key1][key2] = counter
        increment counter

        Use case: create index of error messages
        key1: error type
        key2: error message
        val: error index number
        """
        if key1 in d.keys():
            if key2 in d[key1].keys():
                return
            else:
                d[key1][key2] = self._counter
                self._counter += 1
        else:
            d[key1] = {}
            d[key1][key2] = self._counter
            self._counter += 1
        return

    def view_issubclass(self) -> Observation:
        """Generate results."""
        self.result: Dict[str, Dict[str, int]] = {}
        self.result_alias: Dict[int, str] = {}
        self.result_index: Dict[str, Dict[str, int]] = {}
        job_list: List[Tuple[str, str]] = []
        parsed_obj_1: str
        parsed_obj_2: str
        for i, e in enumerate(list(self.parsed_objs)):
            for w in list(self.parsed_objs)[i:]:
                job_list.append((e, w))
        for job in job_list:
            parsed_obj_1, parsed_obj_2 = job
            for elem_obj_1 in dir(self.parsed_objs[parsed_obj_1]):
                p_elem_obj_1: Any
                p_elem_obj_1 = eval("self.parsed_objs[parsed_obj_1]." + elem_obj_1)
                for elem_obj_2 in dir(self.parsed_objs[parsed_obj_2]):
                    p_elem_obj_2: Any
                    p_elem_obj_2 = eval("self.parsed_objs[parsed_obj_2]." + elem_obj_2)
                    try:
                        if issubclass(p_elem_obj_1, p_elem_obj_2):
                            self._update_dict_inplace(
                                self.result, elem_obj_1, elem_obj_2, "Y"
                            )
                        else:
                            self._update_dict_inplace(
                                self.result, elem_obj_1, elem_obj_2, "N"
                            )
                    # TODO: enable split table by job:
                    # "oov typing dis" should enable displaying 3 distinct tables.
                    # optionally can be chosen split or not split but with namespaces
                    except Exception as err:
                        self._update_enumerated_dict(
                            self.result_index, err.__class__.__name__, str(err)
                        )
                        self._update_dict_inplace(
                            self.result,
                            elem_obj_1,
                            elem_obj_2,
                            self.result_index[err.__class__.__name__][str(err)],
                        )

        return Observation(self.result, self.result_index)
