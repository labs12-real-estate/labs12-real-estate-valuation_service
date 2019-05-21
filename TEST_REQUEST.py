import json
import requests

def main():

    def location(service: str) -> str:
        ''' service is either 'aws' or 'local'
        returns a url'''

        if service=='local':
            return "http://localhost:5000/"
        elif service=='aws':
            return "http://HouseMvp-env.9zyhxaxxek.us-east-1.elasticbeanstalk.com/"
        else:
            raise Exception("SERVICE NOT FOUND. ")

    url = location("local")

    good_address = "3400 Pacific Ave., Marina Del Rey, CA, 90292"
    bad_address = "7543 Heron Hill Dr. Downingtown Michigan 19335"

    good_addr = {'address': good_address}
    r_good = requests.post(url, data=json.dumps(good_addr))

    print(f"good address responded: {r_good}.\nthe content of the resonse was {r_good.json()}")

    bad_addr = {'address': bad_address}
    r_bad = requests.post(url, data=json.dumps(bad_addr))

    print(f"the bad address responded: {r_bad}.\nthe content of the resonse was {r_bad.json()}")

    survey_data = {
            "address": "12345 Butternut Avenue, Sand Lake, MI 49343",
            "countertops": "laminate",
            "flooring": "hardwood",
            "roofAge": "0-4 years",
            "furnaceAge": "0-4 years"
        }

    r_survey = requests.post(url+"survey", data=json.dumps(survey_data))

    print(f"The survey responded: {r_survey}.\nThe content of the repsonse was {r_survey.json()}")

    pass

if __name__=='__main__': 
    main()
