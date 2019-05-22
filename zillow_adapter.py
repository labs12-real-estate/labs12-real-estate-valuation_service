#!/usr/bin/env python

import os
import re
from typing import List, Optional, Union, Tuple
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pyzillow.pyzillowerrors import ZillowError
from functools import reduce
def times(x, y): return x*y
product = lambda xs: reduce(times, xs)

def addr_zip_split(raw_add: str) -> Tuple[str, str]:
    zippat = r'[0-9]{5}$'
    zipcode = re.search(zippat, raw_add).group()
    address = raw_add[:(len(raw_add) - len(zipcode) - 1)]
    return address, zipcode

ZILLOW_KEY = "X1-ZWz1h2y9e516ob_6plsv" #os.environ['ZWSID']

PingZillow = Optional[GetDeepSearchResults]

class ask_zillow:
    ''' a quasi adapter class for the zillow api. '''
    def __init__(self, address: str, zipcode: str, credential: str = ZILLOW_KEY):
        self.address: str = address
        self.zipcode: Union[str, int] = zipcode
        self.zillow: ZillowWrapper = ZillowWrapper(credential)
        self.results: PingZillow = self.results_()

    def results_(self) -> PingZillow:
        try:
            deep_search_response = (self
                                    .zillow
                                    .get_deep_search_results(
                                        self.address,
                                        self.zipcode))
            return GetDeepSearchResults(deep_search_response)

        except ZillowError:
            return None

# Test = ask_zillow("42 Heron Hill Dr. Downingtown, PA", 19335)
