# Usage

## Location: `valuate.us-east-1.elasticbeanstalk.com`

## _on the route_ `/`: 
- please send object ```{'address': '77 main street town state 54321'}```

Along a `200`, you will **either** receive: 
- `{'low': 10, 
'high': 100, 
'parcel': {a {big {complicated { object }}}},
'address': '77 main street town state 54321'}`
where `low` and `high` are the model's valuation, **or**
- `{'FAIL': 'pyzillow rejected this address. '}`

## _on the route_ `/survey`
- please send the object ```{
    "address": "123 local road townsville pa 56789"
    "countertops": "laminate",
	  "flooring": "hardwood",
	  "roofAge": "0-4 years",
	  "furnaceAge": "0-4 years"
    }```

- _along a `200` you will receive_ `{'value': 100, 'low': 75, 'high': 125}`
  where `value` is the central estimate, and `low`/`high` are the range as
  before. 

There's a very broad error handler here, if something goes wrong it will _send
along a `200`_ the message "Failed because whatever thing went wrong". 

**Notice**: We are assuming that no bad addresses will be passed to the second
route! If this assumption is unwise, please let me know and i'm happy to add
error handling. 

**Notice**: This is dependent on a serialized model and dataframe, which are not
available on github, so you can't run it yourself. As of this writing it is live
on an elastic beanstalk at the above address.  
