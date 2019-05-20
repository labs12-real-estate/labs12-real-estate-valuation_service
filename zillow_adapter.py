#!/usr/bin/env python

import os
from typing import List, Optional, Union
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pyzillow.pyzillowerrors import ZillowError
from xml.etree.ElementTree import Element

ZILLOW_KEY = "X1-ZWz1h2y9e516ob_6plsv" #os.environ['ZWSID']

PingZillow = Optional[GetDeepSearchResults]
zillow_data = ZillowWrapper(ZILLOW_KEY)

class ask_zillow:
    ''' a quasi adapter class for the zillow api. '''
    def __init__(self, address: str, zipcode: str, credential: str = ZILLOW_KEY):
        self.address: str = address
        self.zipcode: Union[str, int] = zipcode
        self.zillow: ZillowWrapper = ZillowWrapper(credential)
        self.results: Optional[Element] = self.results_()
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

X = ask_zillow("42 Heron Hill Dr. Downingtown, PA", 19335)
