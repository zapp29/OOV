"""Pytest module testing OOV.py implementation."""
from types import ModuleType
from typing import Dict

import pytest

from oov.oov import OOV

# TODO: test that OOV can be used with: "import oov"
# TODO: test on all multiple builtin modules if the program doesn't fail


class TestCreateObject:
    """Test __init__ method."""

    class TestTwoPackagesImpTrue:
        """TEST CASE 1.

        Test correctly specified parameters:
        - two different packages
        - imp: True
        """

        def test_object_length(self) -> None:
            """Checks if object len() is as desired."""
            result_1 = len(OOV(["collections.abc", "typing"]).parsed_objs)
            assert result_1 == 2

        def test_object_keys(self) -> None:
            """Checks if object has proper keys."""
            result_1 = list(OOV(["collections.abc", "typing"]).parsed_objs)[0]
            result_2 = list(OOV(["collections.abc", "typing"]).parsed_objs)[1]
            assert result_2 == "typing"
            assert result_1 == "collections.abc"

        def test_object_value_types(self) -> None:
            """Checks if object values are of proper type."""
            result_1 = OOV(["collections.abc", "typing"]).parsed_objs["collections.abc"]
            result_2 = OOV(["collections.abc", "typing"]).parsed_objs["typing"]
            assert isinstance(result_1, ModuleType)
            assert isinstance(result_2, ModuleType)

    class TestOnePackageImpTrue:
        """TEST CASE 2.

        Test correctly specified parameters:
        - one package
        - imp: True
        """

        def test_object_length(self) -> None:
            """Checks if object len() is as desired."""
            result_1 = len(OOV("collections.abc").parsed_objs)
            assert result_1 == 1

        def test_object_keys(self) -> None:
            """Checks if object has proper keys."""
            result_2 = list(OOV("collections.abc").parsed_objs)[0]
            assert result_2 == "collections.abc"

        def test_object_value_types(self) -> None:
            """Checks if object values are of proper type."""
            result_3 = OOV("collections.abc").parsed_objs["collections.abc"]
            assert isinstance(result_3, ModuleType)

    class TestTwoPackagesImpFalse:
        """TEST CASE 3.

        Test correctly specified parameters:
        - two packages
        - imp: False
        """

        def test_object_length(self) -> None:
            """Checks if object len() is as desired."""
            import collections.abc
            import typing

            result_1 = len(OOV([collections.abc, typing]).parsed_objs)
            assert result_1 == 2

        def test_object_keys(self) -> None:
            """Checks if object has proper keys."""
            import collections.abc
            import typing

            result_1 = list(OOV([collections.abc, typing]).parsed_objs)[0]
            result_2 = list(OOV([collections.abc, typing]).parsed_objs)[1]
            assert result_2 == "typing"
            assert result_1 == "collections.abc"

        def test_object_value_types(self) -> None:
            """Checks if object values are of proper type."""
            import collections.abc
            import typing

            result_1 = OOV([collections.abc, typing]).parsed_objs["collections.abc"]
            result_2 = OOV([collections.abc, typing]).parsed_objs["typing"]
            assert isinstance(result_1, ModuleType)
            assert isinstance(result_2, ModuleType)

    class TestOnePackageImpFalse:
        """TEST CASE 4.

        Test correctly specified parameters:
        - one package:
            - as module,
            - as list,
        - imp: False
        """

        def test_object_length(self) -> None:
            """Checks if object len() is as desired."""
            import collections.abc

            result_1 = len(OOV([collections.abc]).parsed_objs)
            result_2 = len(OOV(collections.abc).parsed_objs)
            assert result_1 == 1
            assert result_2 == 1

        def test_object_keys(self) -> None:
            """Checks if object has proper keys."""
            import collections.abc

            result_1 = list(OOV([collections.abc]).parsed_objs)[0]
            result_2 = list(OOV(collections.abc).parsed_objs)[0]
            assert result_1 == "collections.abc"
            assert result_2 == "collections.abc"

        def test_object_value_types(self) -> None:
            """Checks if object values are of proper type."""
            import collections.abc

            result_1 = OOV([collections.abc]).parsed_objs["collections.abc"]
            result_2 = OOV(collections.abc).parsed_objs["collections.abc"]
            assert isinstance(result_1, ModuleType)
            assert isinstance(result_2, ModuleType)

    class TestVariousIncorrectParams:
        """TEST CASE 5.

        Test incorrectly specified parameters:
        - wrong type
        - inexisting module as string
        """

        def test_wrong_type(self) -> None:
            """Checks if the objects behaviour when wrong type is passed."""
            with pytest.raises(TypeError):
                OOV([12])  # type: ignore
            with pytest.raises(TypeError):
                OOV(True)  # type: ignore

        def test_inexisting_package_as_string(self) -> None:
            """Checks if the objects behaviour when inexisting package is passed."""
            with pytest.raises(ModuleNotFoundError):
                OOV("pythonsucks")


class TestUpdateDictInplace:
    """Test _update_dict_inplace method."""

    def test__update_dict_inplace(self) -> None:
        """Checks _update_dict dictionary manipulation function."""
        d: Dict[str, Dict[str, int]] = {}
        obj = OOV("collections.abc")
        obj._update_dict_inplace(d, "k1", "k2", 123)
        assert d["k1"]["k2"] == 123
        obj._update_dict_inplace(d, "k1", "k2", 321)
        assert d["k1"]["k2"] == 321
        obj._update_dict_inplace(d, "k1", "k3", 1234)
        assert d["k1"]["k3"] == 1234
        obj._update_dict_inplace(d, "k4", "k2", 4321)
        assert d["k4"]["k2"] == 4321


class TestUpdateEnumeratedDict:
    """Test _update_dict_inplace method."""

    def test__update_enumerated_dict(self) -> None:
        """Checks _update_enumerated_dict dictionary manipulation function."""
        d: Dict[str, Dict[str, int]] = {}
        obj = OOV("collections.abc")
        obj._update_enumerated_dict(d, "k1", "k2")
        assert d["k1"]["k2"] == 1
        obj._update_enumerated_dict(d, "k1", "k2")
        assert d["k1"]["k2"] == 1
        obj._update_enumerated_dict(d, "k1", "k3")
        assert d["k1"]["k3"] == 2
        obj._update_enumerated_dict(d, "k1", "k3")
        assert d["k1"]["k3"] == 2
        obj._update_enumerated_dict(d, "k4", "k2")
        assert d["k4"]["k2"] == 3
        obj._update_enumerated_dict(d, "k4", "k2")
        assert d["k4"]["k2"] == 3


class TestViewIssubclass:
    """Test view_issubclass method."""

    def test_view_issubclass(self) -> None:
        """Checks if view_issubclass methods returns proper values."""
        import tests.input.dummy_module as dummy_module  # type: ignore

        obj = OOV(dummy_module)
        result = obj.view_issubclass()
        result = result.get_data()

        assert result["MainClass1"]["MainClass1"] == "Y"
        assert result["MainClass2"]["MainClass2"] == "Y"
        assert result["MainClass3"]["MainClass3"] == "Y"

        assert result["ChildClass1"]["ChildClass1"] == "Y"
        assert result["ChildClass2"]["ChildClass2"] == "Y"

        assert result["ChildClass1"]["MainClass1"] == "Y"
        assert result["ChildClass1"]["MainClass2"] == "Y"
        assert result["ChildClass1"]["MainClass3"] == "Y"
        assert result["ChildClass1"]["MainClass4"] == "N"

        assert result["ChildClass2"]["MainClass1"] == "Y"
        assert result["ChildClass3"]["MainClass1"] == "Y"
        assert result["ChildClass5"]["MainClass1"] == "N"

        assert result["ChildClass5"]["MainClass4"] == "Y"

        assert result["ChildClass6"]["MainClass5"] == "Y"
        assert result["ChildClass7"]["MainClass6"] == "Y"
        assert result["ChildClass8"]["MainClass7"] == "Y"

        assert result["MainClass1"]["ChildClass1"] == "N"
        assert result["ChildClass2"]["ChildClass1"] == "N"
