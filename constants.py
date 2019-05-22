#!/usr/bin/env python
from typing import Optional, Tuple
import re
import pickle
from collections import namedtuple
from functools import reduce
from itertools import chain
from pyzillow.pyzillow import GetDeepSearchResults
import pandas as pd

with open("final_df.pickle", "rb") as fp:
    X_, y = pickle.load(fp)

def prep(dat: pd.DataFrame) -> pd.DataFrame:

    return (dat.drop(['zip5_encoded', 'city_encoded'], axis=1)
            .rename(columns={'year_built_bin': 'year_built', 'baths_lavs': 'bathrooms', 'beds_total': 'bedrooms'})
            .assign(**{feat: pd.cut(dat[feat],
                                    bins=[0, 4, 9, 14, 10000],
                                    labels=["0-4 years", "5-9 years", "10-14 years", "15+"])
                       for feat
                       in ['roof_year', 'furnace_year']})
            .reindex(['bedrooms', 'bathrooms', 'year_built',
                      'quartz_countertops', 'granite_countertops', 'formica_countertops', 'tile_countertops',
                      'laminate_floors', 'hardwood_floors'], axis=1))

X = prep(X_)

def list_sum(*xss):
    ''' takes an *args of lists and returns the concatenation'''
    return reduce(lambda ls, ms: ls+ms, xss)

def addr_zip_split(raw_add: str) -> Tuple[str, str]:
    ''' takes a string that's address into zipcode, returns addr and zip as tuple. '''
    zippat = r'[0-9]{5}$'
    zipcode = re.search(zippat, raw_add).group()
    address = raw_add[:(len(raw_add) - len(zipcode) - 1)]
    return address, zipcode

SurveyPredictants = namedtuple("SurveyPredictants",
                               ["countertops", "flooring", "roof_age", "furnace_age"])

PingZillow = Optional[GetDeepSearchResults]
ZILLOW_KEY = "X1-ZWz1h2y9e516ob_6plsv" #os.environ['ZWSID']
NULL = 'skip' # alias for none


COUNTERTOPS_MAP = {"Marble/Quartz": [1, 0, 0, 0],
                   "Granite/Concrete": [0, 1, 0, 0],
                   '"Formica/Tile"': [0, 0, 1, 1],
                   'Laminate': [0, 0, 0, 0],
                   'skip': [X.quartz_countertops.mean(),
                            X.granite_countertops.mean(),
                            X.formica_countertops.mean(),
                            X.tile_countertops.mean()]}

FLOORING_MAP = {"Hardwood" : [0, 1],
                "Engineered/Laminate": [1, 0],
                "Ceramic Tile": [0, 0],
                "Porcelain Tile/Concrete": [0, 0],
                "skip": [X.laminate_floors.mean(),
                         X.hardwood_floors.mean()]}

ROOF_FURNACE_MAP = {**{'skip': [y.mean()]}, **{feat: [feat]
                                             for feat
                                             in ["0-4 years", "5-9 years", "10-14 years", "15+"]}}

