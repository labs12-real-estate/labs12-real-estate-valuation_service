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


def addr_zip_split(raw_add: str) -> Tuple[str, str]:
    zippat = r'[0-9]{5}$'
    zipcode = re.search(zippat, raw_add).group()
    address = raw_add[:(len(raw_add) - len(zipcode) - 1)]
    return address, zipcode


application = app = Flask(__name__)
app.config['TESTING'] = True
CORS(app)

@app.route("/", methods=['POST'])
def get() -> Response:
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

        predictands: List[float] = [
            result.home_size,
            result.bedrooms,
            result.bathrooms]

        #valuation: float = sum(predictants)# rfr.model.predict(np.array([predictants]))[0]

        outdat = {'arbitrary-function-of-predictants': str(predictands)}

        print(outdat)

        return app.response_class(
            response=json.dumps(outdat),
            status=200,
            mimetype='application/json'
        )


if __name__ == '__main__':
    app.run(debug=True)
