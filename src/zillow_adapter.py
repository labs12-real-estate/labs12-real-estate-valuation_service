#!/usr/bin/env python

import os
import re
from typing import List, Optional, Union, Tuple
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pyzillow.pyzillowerrors import ZillowError
from constants import PingZillow, ZILLOW_KEY



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
            res = GetDeepSearchResults(deep_search_response)
            #if not res.property_size:
            #    return None
            #else:
            #    return res
            return res

        except ZillowError:
            return None

# Test = ask_zillow("42 Heron Hill Dr. Downingtown, PA", 19335)
