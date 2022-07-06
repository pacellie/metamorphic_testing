# Based on https://thecleverprogrammer.com/2020/12/29/house-price-prediction-with-python/
from pathlib import Path

import numpy as np
import pandas as pd

# sklearn has no typing stubs, so mypy would usually complain
from sklearn.base import BaseEstimator, TransformerMixin  # type: ignore
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit  # type: ignore
from sklearn.preprocessing import OneHotEncoder  # type: ignore
from sklearn.pipeline import Pipeline  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore
from sklearn.impute import SimpleImputer  # type: ignore
from sklearn.compose import ColumnTransformer  # type: ignore

from hypothesis import given
import hypothesis.strategies as st

from metamorphic_test import transform, relate
from metamorphic_test.transformation import MetamorphicTransformation
from metamorphic_test.relation import MetamorphicRelation
from metamorphic_test.relations import GreaterThan, ApproxEqual


csv_path = Path(__file__).parent / "housing.csv"
housing = pd.read_csv(csv_path)
housing.head()

train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

housing['income_cat'] = pd.cut(
    housing['median_income'],
    bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
    labels=[1, 2, 3, 4, 5]
)
# plot histogram:
# housing['income_cat'].hist()


split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

for set_ in (strat_train_set, strat_test_set):
    set_.drop('income_cat', axis=1, inplace=True)
housing = strat_train_set.copy()

housing["rooms_per_household"] = housing["total_rooms"]/housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"]/housing["total_rooms"]
housing["population_per_household"] = housing["population"]/housing["households"]

corr_matrix = housing.corr()

# Data Preparation
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

median = housing["total_bedrooms"].median()
housing["total_bedrooms"].fillna(median, inplace=True)

housing_num = housing.drop("ocean_proximity", axis=1)

# column index
rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True): # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, *_):
        return self  # nothing else to do
    def transform(self, X):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household,
                         bedrooms_per_room]
        return np.c_[X, rooms_per_household, population_per_household]


num_pipeline = Pipeline([
    ('imputer',SimpleImputer(strategy="median")),
    ('attribs_adder', CombinedAttributesAdder()),
    ('std_scaler', StandardScaler()),
])
housing_num_tr = num_pipeline.fit_transform(housing_num)


num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]
full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", OneHotEncoder(), cat_attribs),
])
housing_prepared = full_pipeline.fit_transform(housing)


lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

data = housing.iloc[:5]
labels = housing_labels.iloc[:5]
data_preparation = full_pipeline.transform(data)
print(data_preparation)
print("Predictions: ", lin_reg.predict(data_preparation))


#
# Here's where the testing action begins
#


# basic test:

class IncreaseRooms(MetamorphicTransformation[np.ndarray, np.ndarray]):
    def transform(self, anchor: np.ndarray, increase_rooms_by: int = 1) -> np.ndarray:
        copy = anchor.copy()
        NUMBER_OF_ROOMS_INDEX = 3
        copy[NUMBER_OF_ROOMS_INDEX] += increase_rooms_by
        return copy

@given(
    anchor=st.sampled_from(list(data_preparation)),
    increase_rooms_by=st.integers(min_value=1, max_value=10),
)
@transform(IncreaseRooms())
@relate(GreaterThan() | ApproxEqual())
def test_house_pricing_more_rooms(x: np.ndarray) -> float:
    return lin_reg.predict(x.reshape(1, -1))[0]


# vectorized, but with a harder-to-read output:

class IncreaseRoomsVectorized(MetamorphicTransformation[np.ndarray, np.ndarray]):
    def transform(self, anchor: np.ndarray, increase_rooms_by: int = 1) -> np.ndarray:
        copy = anchor.copy()
        NUMBER_OF_ROOMS_INDEX = 3
        copy[NUMBER_OF_ROOMS_INDEX] += increase_rooms_by
        return copy


class NumPyAllAtLeastTheSame(MetamorphicRelation):
    def relate_check(self, a: np.ndarray, b: np.ndarray) -> None:
        assert np.all(a <= b)


@given(
    anchor=st.just(data_preparation),
    increase_rooms_by=st.integers(min_value=1, max_value=10),
)
@transform(IncreaseRoomsVectorized())
@relate(NumPyAllAtLeastTheSame())
def test_house_pricing_more_rooms_vectorized(x: np.ndarray) -> float:
    return lin_reg.predict(x)
