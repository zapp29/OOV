from oov import OOV
from types import ModuleType
import pytest


class TestCreate_TwoPackagesImpTrue:
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


class TestCreate_OnePackageImpTrue:
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


class TestCreate_TwoPackagesImpFalse:
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


class TestCreate_OnePackageImpFalse:
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

class TestCreate_VariousIncorrectParams:
    """TEST CASE 5.

    Test incorrectly specified parameters:
    - wrong type
    - inexisting module:
        - as module,
        - as string
    """
    def test_wrong_type(self):
        with pytest.raises(TypeError):
            OOV([12])
        with pytest.raises(TypeError):
            OOV(True)

    def test_inexisting_package_as_module(self):
        pass

    def test_inexisting_package_as_string(self):
        pass

