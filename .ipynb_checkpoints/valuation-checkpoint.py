#!/usr/bin/env python

from zillow_adapter import PingZillow
from typing import Tuple

class valuation:
    def __init__(self, zillow: PingZillow):
        self.zillow: PingZillow = zillow
        self.valuation: Tuple[float, float]
