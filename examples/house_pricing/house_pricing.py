# Based on https://thecleverprogrammer.com/2020/12/29/house-price-prediction-with-python/
from pathlib import Path

import numpy as np
import pandas as pd

# sklearn has no typing stubs, so mypy would usually complain
from sklearn.model_selection import StratifiedShuffleSplit  # type: ignore
from sklearn.preprocessing import OneHotEncoder  # type: ignore
from sklearn.pipeline import Pipeline  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore
from sklearn.impute import SimpleImputer  # type: ignore
from sklearn.compose import ColumnTransformer  # type: ignore



def add_basic_calculations(housing) -> None:
    """
    Adds basic calculations to the housing data in place.
    This includes: rooms per household, bedrooms per room, population per household,
    """
    housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
    housing["bedrooms_per_room"] = housing["total_bedrooms"] / housing["total_rooms"]
    housing["population_per_household"] = housing["population"] / housing["households"]
    return housing


def fill_bedroom_number(housing):
    """
    Fills in the bedroom number with the median value of the bedroom number in place.
    """
    housing["total_bedrooms"].fillna(housing["total_bedrooms"].median(), inplace=True)


def get_housing_data():
    csv_path = Path(__file__).parent / "housing.csv"
    housing = pd.read_csv(csv_path)
    housing.head()
    add_basic_calculations(housing)
    fill_bedroom_number(housing)
    return housing


def add_income_category(housing) -> None:
    """
    Modifies housing data in place to also include an income_cat
    which is the income category of the median income.
    """
    housing['income_cat'] = pd.cut(
        housing['median_income'],
        bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
        labels=[1, 2, 3, 4, 5]
    )

def remove_income_category(housing):
    """
    Removes the income_cat column from the housing data in place.
    """
    housing.drop(columns=["income_cat"], axis=1, inplace=True)


def get_training_and_test_set(housing):
    """
    Returns a stratified sampling on the housing data.
    Why this is necessary:
    https://thecleverprogrammer.com/2020/12/22/stratified-sampling-with-python/
    """
    # we will split by income category and temporarily add it for that purpose
    add_income_category(housing)

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(housing, housing["income_cat"]):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]
    
    remove_income_category(housing)
    return strat_train_set, strat_test_set


def hide_labels(housing):
    """
    Hides the labels from the housing data in place
    and returns the labels.
    """
    labels = housing["median_house_value"].copy()
    housing.drop(columns=["median_house_value"], axis=1, inplace=True)
    return labels


def create_pipeline(housing):
    housing_num = housing.drop("ocean_proximity", axis=1)
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy="median")),
        ('std_scaler', StandardScaler()),
    ])
    # housing_num_tr = num_pipeline.fit_transform(housing_num)
    num_attribs = list(housing_num)
    cat_attribs = ["ocean_proximity"]
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
        ("cat", OneHotEncoder(), cat_attribs),
    ])
    full_pipeline.fit_transform(housing)
    return full_pipeline


def prepare_housing_data(housing):
    return create_pipeline(housing).fit_transform(housing)


def create_linear_regression_model(housing):
    labels = hide_labels(housing)
    housing_prepared = prepare_housing_data(housing)
    lin_reg = LinearRegression()
    lin_reg.fit(housing_prepared, labels)
    return lin_reg


class HousingPricePredictor:
    def __init__(self, housing):
        self.lin_reg = create_linear_regression_model(housing)
        self.pipeline = create_pipeline(housing)

    def predict(self, data):
        return self.lin_reg.predict(self.pipeline.transform(data))


if __name__ == '__main__':
    training_set, test_set = get_training_and_test_set(get_housing_data())
    p = HousingPricePredictor(training_set)
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info("Predictions: %s", p.predict(test_set))