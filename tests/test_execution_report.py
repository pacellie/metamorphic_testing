import pytest

from metamorphic_test.report.execution_report import MetamorphicExecutionReport
from metamorphic_test.metamorphic import PrioritizedTransform


@pytest.fixture
def generic_p_transform():
    def transform(x):
        return x
    return PrioritizedTransform(transform, 0)


@pytest.fixture
def generic_m_report():
    def system(x):
        return x

    def relation(_):
        return True

    return MetamorphicExecutionReport(0, system, relation)


@pytest.mark.parametrize("number_of_transforms", range(5))
def test_transform_results_len(
    number_of_transforms, 
    generic_p_transform,
    generic_m_report
):
    test_transforms = [generic_p_transform for _ in range(number_of_transforms)]
    generic_m_report.transforms = test_transforms
    assert len(generic_m_report.transforms) == number_of_transforms
    assert len(generic_m_report.transform_results) == number_of_transforms, \
        "transform_results should be filled"

def test_register_transform_result(
    generic_p_transform,
    generic_m_report
):
    test_transforms = [generic_p_transform for _ in range(5)]
    generic_m_report.transforms = test_transforms
    for i in (0, 3, 4):
        with generic_m_report.register_transform_result(i) as set_:
            set_("test")
        assert generic_m_report.transform_results[i].output == "test", \
            "transform_results should be filled"

def test_register_transform_result_out_of_range(
    generic_p_transform,
    generic_m_report
):
    test_transforms = [generic_p_transform for _ in range(5)]
    generic_m_report.transforms = test_transforms
    with pytest.raises(IndexError):
        with generic_m_report.register_transform_result(15):
            pass

class _TestException(Exception):
    pass

def test_register_transform_error(
    generic_p_transform,
    generic_m_report
):
    test_transforms = [generic_p_transform for _ in range(5)]
    generic_m_report.transforms = test_transforms
    for i in (0, 3, 4):
        with pytest.raises(_TestException):
            with generic_m_report.register_transform_result(i):
                raise _TestException("test")
        assert generic_m_report.transform_results[i].error is not None, \
            "transform_results errors should be filled"

def test_register_output_x(
    generic_m_report
):
    with generic_m_report.register_output_x() as set_:
        set_("test")
    assert generic_m_report.output_x.output == "test", \
        "output_x should be filled"

def test_register_output_x_error(
    generic_m_report
):
    with pytest.raises(_TestException):
        with generic_m_report.register_output_x():
            raise _TestException("test")
    assert generic_m_report.output_x.error is not None, \
        "output_x error should be filled"

def test_register_output_y(
    generic_m_report
):
    with generic_m_report.register_output_y() as set_:
        set_("test")
    assert generic_m_report.output_y.output == "test", \
        "output_y should be filled"

def test_register_output_y_error(
    generic_m_report
):
    with pytest.raises(_TestException):
        with generic_m_report.register_output_y():
            raise _TestException("test")
    assert generic_m_report.output_y.error is not None, \
        "output_y error should be filled"

def test_register_relation_result(
    generic_m_report
):
    with generic_m_report.register_relation_result() as set_:
        set_(True)
    assert generic_m_report.relation_result.output, \
        "relation_result should be filled"
    with pytest.raises(ValueError):  # cannot set multiple times
        with generic_m_report.register_relation_result() as set_:
            set_(False)

def test_register_relation_result_only_booleans(
    generic_m_report
):
    with pytest.raises(ValueError):
        with generic_m_report.register_relation_result() as set_:
            set_("This is not a boolean, it's a string")