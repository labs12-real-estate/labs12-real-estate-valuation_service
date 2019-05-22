# Location: `valuate.us-east-1.elasticbeanstalk.com`

### Notice: the content of the data is nonsense, we are just testing the routes. 

## _on the route_ `/`: 
- please send object ```{'address': '77 main street town state 54321'}```

Along a `200`, you will **either** receive: 
- `{'low': 10, 
'high': 100, 
'parcel': {a {big {complicated { object }}}},
'address': '77 main street town state 54321'}`
**or**
- `{'FAIL': 'pyzillow rejected this address. '}`

## _on the route_ `/survey`
- please send the object ```{
    "address": "123 local road townsville pa 56789"
    "countertops": "laminate",
	  "flooring": "hardwood",
	  "roofAge": "0-4 years",
	  "furnaceAge": "0-4 years"
    }```

- _along a `200` you will receive_ `{'low': 'a string showing', 'high': 'what
  you just sent'}`

There's a very broad error handler here, if something goes wrong it will _send
along a `200`_ "Failed because thing that went wrong". 

**Notice**: We are assuming that no bad addresses will be passed to the second
route! If this assumption is unwise, please let me know and i'm happy to add
error handling. 
