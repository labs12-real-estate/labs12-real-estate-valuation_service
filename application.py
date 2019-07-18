# -*- coding: utf-8 -*-
''' '''
import json
from typing import List
from flask import Flask, request, Response  # , response_class
from constants import NULL, addr_zip_split, PingZillow, SurveyPredictants
from valuation import valuation

application = app = Flask(__name__)
app.config['TESTING'] = True
#
#
# * * INITIAL VALUATION ROUTE.
#
@app.route("/", methods=['POST'])
def address() -> Response:
    ''' the first route. '''
    from zillow_adapter import ask_zillow
   
    lines = request.get_json(force=True)
    address_: str = lines['address']

    address, zipcode = addr_zip_split(address_)

    result: PingZillow = ask_zillow(address, zipcode).results



    if not result:
        message = "address given not available in zillow api. Please try another address"
        print(message)

        return app.response_class(response=json.dumps({"FAIL": message}),
                                  status=200,
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

        #survey_predictants = SurveyPredictants(NULL, NULL, NULL, NULL)

        #valuator = valuation(result, survey_predictants)

        outdat = {'low': None,  #valuator.low,
                  'high': None, #valuator.high,
                  'parcel': parcel_data,
                  'address': address_}

        print(outdat)

        return app.response_class(
            response=json.dumps(outdat),
            status=200,
            mimetype='application/json'
        )


@app.route("/survey", methods=['POST'])
def survey() -> Response:
    ''' the second route. '''
    from zillow_adapter import ask_zillow

    lines = request.get_json(force=True)

    try:
        countertops = lines['countertops']
        flooring = lines['flooring']
        roof_age = lines['roofAge']
        furnace_age = lines['furnaceAge']
        address_ = lines['address']
        address, zipcode = addr_zip_split(address_)

        survey_predictants = SurveyPredictants(countertops, flooring, roof_age, furnace_age)

        address, zipcode = addr_zip_split(address_)

        result: PingZillow = ask_zillow(address, zipcode).results

        if not result:
            message = "address given not available in zillow api. Please try another address"
            print(message)

            return app.response_class(response=json.dumps({"FAIL": message}),
                                      status=200,
                                      mimetype='application/json'
                                      )
        else:
            valuator = valuation(result, survey_predictants)

            outdat = {'value': valuator.prediction,
                      'low': valuator.low,
                      'high': valuator.high,
                      }

            print("success!\t", outdat)

            return app.response_class(response=json.dumps(outdat),
                                      status=200,
                                      mimetype='application/json')

    except Exception as e:
        print("something wrong.\t", e)

        return app.response_class(response=json.dumps({"Fail": f"Failed because {e}"}),
                                  status=200,
                                  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
