from oov import OOV
from types import ModuleType
import pytest


class TestCreateObject:
    """Test __init__ method."""

    class TestTwoPackagesImpTrue:
        """TEST CASE 1.

        Test correctly specified parameters:
        - two different packages
        - imp: True
        """

        def test_object_length(self):
            result_1 = len(OOV(["pandas", "numpy"]).parsed_objs)
            assert result_1 == 2

        def test_object_keys(self):
            result_1 = list(OOV(["pandas", "numpy"]).parsed_objs)[0]
            result_2 = list(OOV(["pandas", "numpy"]).parsed_objs)[1]
            assert result_2 == "numpy"
            assert result_1 == "pandas"

        def test_object_value_types(self):
            result_1 = OOV(["pandas", "numpy"]).parsed_objs['pandas']
            result_2 = OOV(["pandas", "numpy"]).parsed_objs['numpy']
            assert isinstance(result_1, ModuleType)
            assert isinstance(result_2, ModuleType)

    class TestOnePackageImpTrue:
        """TEST CASE 2.

        Test correctly specified parameters:
        - one package
        - imp: True
        """

        def test_object_length(self):
            result_1 = len(OOV("pandas").parsed_objs)
            assert result_1 == 1

        def test_object_keys(self):
            result_2 = list(OOV("pandas").parsed_objs)[0]
            assert result_2 == "pandas"

        def test_object_value_types(self):
            result_3 = OOV("pandas").parsed_objs['pandas']
            assert isinstance(result_3, ModuleType)

    class TestTwoPackagesImpFalse:
        """TEST CASE 3.

        Test correctly specified parameters:
        - two packages
        - imp: False
        """

        def test_object_length(self):
            import pandas
            import numpy
            result_1 = len(OOV([pandas, numpy]).parsed_objs)
            assert result_1 == 2

        def test_object_keys(self):
            import pandas
            import numpy
            result_1 = list(OOV([pandas, numpy]).parsed_objs)[0]
            result_2 = list(OOV([pandas, numpy]).parsed_objs)[1]
            assert result_2 == "numpy"
            assert result_1 == "pandas"

        def test_object_value_types(self):
            import pandas
            import numpy
            result_1 = OOV([pandas, numpy]).parsed_objs['pandas']
            result_2 = OOV([pandas, numpy]).parsed_objs['numpy']
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

        def test_object_length(self):
            import pandas
            result_1 = len(OOV([pandas]).parsed_objs)
            result_2 = len(OOV(pandas).parsed_objs)
            assert result_1 == 1
            assert result_2 == 1

        def test_object_keys(self):
            import pandas
            result_1 = list(OOV([pandas]).parsed_objs)[0]
            result_2 = list(OOV(pandas).parsed_objs)[0]
            assert result_1 == "pandas"
            assert result_2 == "pandas"

        def test_object_value_types(self):
            import pandas
            result_1 = OOV([pandas]).parsed_objs['pandas']
            result_2 = OOV(pandas).parsed_objs['pandas']
            assert isinstance(result_1, ModuleType)
            assert isinstance(result_2, ModuleType)

    class TestVariousIncorrectParams:
        """TEST CASE 5.

        Test incorrectly specified parameters:
        - wrong type
        - inexisting module as string
        """

        def test_wrong_type(self):
            with pytest.raises(TypeError):
                OOV([12])
            with pytest.raises(TypeError):
                OOV(True)

        def test_inexisting_package_as_string(self):
            with pytest.raises(ModuleNotFoundError):
                OOV("pythonsucks")

class TestUpdateDictInplace:
    """Test _update_dict_inplace method."""

    def test__update_dict_inplace(self):
        d = {}
        obj = OOV("pandas")
        obj._update_dict_inplace(d, "k1", "k2", 123)
        assert d["k1"]["k2"] == 123
        obj._update_dict_inplace(d, "k1", "k2", 321)
        assert d["k1"]["k2"] == 321
        obj._update_dict_inplace(d, "k1", "k3", 1234)
        assert d["k1"]["k3"] == 1234
        obj._update_dict_inplace(d, "k4", "k2", 4321)
        assert d["k4"]["k2"] == 4321

class TestViewIssubclass:
    """Test view_issubclass method."""

    def test_view_issubclass(self):
        import input.dummy_module as dummy_module
        obj = OOV(dummy_module)
        result = obj.view_issubclass()
        
        assert result['MainClass1']['MainClass1'] == 1
        assert result['MainClass2']['MainClass2'] == 1
        assert result['MainClass3']['MainClass3'] == 1

        assert result['ChildClass1']['ChildClass1'] == 1
        assert result['ChildClass2']['ChildClass2'] == 1

        assert result['ChildClass1']['MainClass1'] == 1
        assert result['ChildClass1']['MainClass2'] == 1
        assert result['ChildClass1']['MainClass3'] == 1
        assert result['ChildClass1']['MainClass4'] == 0

        assert result['ChildClass2']['MainClass1'] == 1
        assert result['ChildClass3']['MainClass1'] == 1
        assert result['ChildClass5']['MainClass1'] == 0

        assert result['ChildClass5']['MainClass4'] == 1

        assert result['ChildClass6']['MainClass5'] == 1
        assert result['ChildClass7']['MainClass6'] == 1
        assert result['ChildClass8']['MainClass7'] == 1

        assert result['MainClass1'] ['ChildClass1'] == 0
        assert result['ChildClass2']['ChildClass1'] == 0
