# -*- coding: utf-8 -*-
''' '''
from flask import Flask, request, jsonify, Response  # , response_class
from flask_cors import CORS
import json
import pickle
import numpy as np
from typing import List, Tuple, Optional
import re
from pyzillow.pyzillow import GetDeepSearchResults # type: ignore
import os
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
from zillow_adapter import ask_zillow, PingZillow
from functools import reduce
def times(x, y): return x*y
product = lambda xs: reduce(times, xs)

def addr_zip_split(raw_add: str) -> Tuple[str, str]:
    zippat = r'[0-9]{5}$'
    zipcode = re.search(zippat, raw_add).group()
    address = raw_add[:(len(raw_add) - len(zipcode) - 1)]
    return address, zipcode


application = app = Flask(__name__)
app.config['TESTING'] = True
CORS(app)

@app.route("/survey", methods=['POST'])
def survey() -> Response:

    lines = request.get_json(force=True)


    try:
        countertops = lines['countertops']
        flooring = lines['flooring']
        roofAge = lines['roofAge']
        furnaceAge = lines['furnaceAge']

        outdat = {'valuation': countertops + flooring + roofAge + furnaceAge}

        print("success!\t", outdat)

        return app.response_class(response=json.dumps(outdat),
                                  status=200,
                                  mimetype='application/json')

    except Exception as e:
        print("something wrong.\t", e)

        return app.response_class(response=json.dumps({"failed": f"because {e}"}))

@app.route("/", methods=['POST'])
def address() -> Response:
    lines = request.get_json(force=True)
    address_: str = lines['address']

    address, zipcode = addr_zip_split(address_)

    result: PingZillow = ask_zillow(address, zipcode).results

    if not result:
        message = "address given not available in zillow api. Please try another address"
        print(message)

        return app.response_class(response=json.dumps({"FAIL": message}),
                                  status=404,
                                  mimetype='application/json'
                                  )

    else:
        # extract zillow parcel data from zillow deep search
        keys = ['latitude', 'longitude', 'tax_year', 'tax_value', 'year_built',
                'property_size', 'home_size', 'bathrooms', 'bedrooms', 'last_sold_date',
                'last_sold_price', 'zestimate_amount', 'zestimate_last_updated',
                'zestimate_value_change', 'zestimate_valuation_range_high',
                'zestimate_valuationRange_low', 'zestimate_percentile']

        parcel_data = {k: vars(result)[k] for k in keys}


        predictands: List[str] = [
            result.home_size,
            result.bedrooms,
            result.bathrooms]

        #valuation: float = sum(predictants)# rfr.model.predict(np.array([predictants]))[0]

        outdat = {'low': sum(float(x) for x in predictands),
                  'high': product(float(x) for x in predictands),
                  'parcel': parcel_data}

        print(outdat)

        return app.response_class(
            response=json.dumps(outdat),
            status=200,
            mimetype='application/json'
        )


if __name__ == '__main__':
    app.run(debug=True)
