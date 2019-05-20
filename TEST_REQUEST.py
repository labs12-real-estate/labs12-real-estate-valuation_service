import json
import requests

def main(): 
    url_loc = "http://localhost:5000/"# "http://127.0.0.1:5000/"
    #aws_loc = "http://HouseMvp-env.9zyhxaxxek.us-east-1.elasticbeanstalk.com"

    good_address = "3400 Pacific Ave., Marina Del Rey, CA, 90292"
    bad_address = "7543 Heron Hill Dr. Downingtown Michigan 19335"

    data = {'address': good_address}
    r = requests.post(url_loc, data=json.dumps(data))

    print(f"good address responded: {r}.\nthe content of the resonse was {r.json()}")

    data = {'address': bad_address}
    r = requests.post(url_loc, data=json.dumps(data))

    print(f"the bad address responded: {r}.\nthe content of the resonse was {r.json()}")
    pass

if __name__=='__main__': 
    main()
