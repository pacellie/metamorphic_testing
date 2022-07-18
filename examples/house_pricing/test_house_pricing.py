import numpy as np
import pytest

from metamorphic_test import (
    transformation,
    metamorphic,
    system,
    randomized,
)
from metamorphic_test.generators import RandInt
from metamorphic_test.relations import becomes_larger, approximately, or_

from .house_pricing import (
    HousingPricePredictor,
    get_housing_data,
    get_training_and_test_set,
    hide_labels,
)


housing = get_housing_data()
training_set, test_set = get_training_and_test_set(get_housing_data())
p = HousingPricePredictor(training_set)
hide_labels(test_set)  # otherwise this MT would be somewhat pointless

HousePriceTest = metamorphic(
    'HousePriceTest', 
    relation=or_(approximately, becomes_larger)
)

@transformation(HousePriceTest)
@randomized('increase_rooms_by', RandInt(1, 10))
def transform(x, increase_rooms_by: int) -> np.ndarray:
    assert all(x["total_rooms"] % 1 == 0)
    copy = x.copy()
    copy["total_rooms"] += increase_rooms_by
    return copy


@pytest.mark.parametrize(
    'x',
    [test_set.iloc[n:n+1] for n in range(20)],
)
@system(name=HousePriceTest)
def test_house_pricing_more_rooms(x) -> float:
    assert all(x["total_rooms"] % 1 == 0)
    return p.predict(x)