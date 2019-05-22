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
        self.zillow: PingZillow = zillow

        self.countertops = COUNTERTOPS_MAP[survey_predictants.countertops]
        self.flooring = FLOORING_MAP[survey_predictants.flooring]
        self.roof = ROOF_FURNACE_MAP[survey_predictants.roof_age]
        self.furnace = ROOF_FURNACE_MAP[survey_predictants.furnace_age]

        self.surveyed = [self.countertops] + [self.flooring] + [self.roof] + [self.furnace]

        if not self.zillow.year_built:
            self.zillow.year_built = X.year_built.mean()
        if not self.zillow.bedrooms:
            self.zillow.bedrooms = X.bedrooms.mean()
        if not self.zillow.bathrooms:
            self.zillow.bathrooms = X.bathrooms.mean()

        self.predictants = array([[float(self.zillow.bedrooms),
                                  float(self.zillow.bathrooms),
                                  float(self.zillow.year_built)] + \
                                 self.surveyed])

        self.home_size = self.zillow.property_size
       
        self.prediction = None
        self.low = None
        self.high = None
