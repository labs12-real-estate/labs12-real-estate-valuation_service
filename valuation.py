#!/usr/bin/env python

from typing import Tuple, List
from itertools import chain
from constants import *
from numpy import divide, array

class valuation:
    def __init__(self,
                 zillow: PingZillow,
                 survey_predictants = SurveyPredictants(NULL, NULL,
                                                        NULL, NULL)):
        assert zillow is not None, "This address is bad. "
        try:
            with open("model.pickle", "rb") as m:
                self.gbr = pickle.load(m)
        except AttributeError as e:
            print("no model!")

        self.zillow: PingZillow = zillow

        self.countertops = COUNTERTOPS_MAP[survey_predictants.countertops]
        self.flooring = FLOORING_MAP[survey_predictants.flooring]
        self.roof = ROOF_FURNACE_MAP[survey_predictants.roof_age]
        self.furnace = ROOF_FURNACE_MAP[survey_predictants.furnace_age]

        self.surveyed = self.countertops + self.flooring + self.roof + self.furnace

        if not self.zillow.year_built:
            self.zillow.year_built = X.year_built.mean()
        if not self.zillow.bedrooms:
            self.zillow.bedrooms = X.bedrooms.mean()
        if not self.zillow.bathrooms:
            self.zillow.bathrooms = X.bathrooms.mean()

        self.predictants_ = chain([float(self.zillow.bedrooms),
                                   float(self.zillow.bathrooms),
                                   float(self.zillow.year_built)],
                                  self.surveyed)

        # needs [:-2] because encoder broken.
        self.predictants = array(list(self.predictants_)[:-2]).reshape(-1,1).T

        try:
            # Not all houses have property size attribute in zillow
            self.home_size = float(self.zillow.property_size)
        except TypeError as e:
            self.home_size = None

        self.half_stdv = divide(y.std(), 2)
        self.prediction_psqft = self.gbr.predict(self.predictants)[0]
        self.low_psqft = self.prediction_psqft - self.half_stdv
        self.high_psqft = self.prediction_psqft + self.half_stdv

        try:
            ## will multiply a number by None if the property size attribute is unavailable.
            self.prediction = self.prediction_psqft * self.home_size
            self.low = self.low_psqft * self.home_size
            self.high = self.high_psqft * self.home_size

        except TypeError as e:
            self.prediction = f"price per square foot valuation is {self.prediction_psqft}"
            self.low = f"price per square foot low is {self.low_psqft}"
            self.high = f"price per square foot high is {self.high_psqft}"
