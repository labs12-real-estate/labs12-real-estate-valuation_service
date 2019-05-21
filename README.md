# Location: `valuator.us-east-1.elasticbeanstalk.com`

### Notice: the content of the data is nonsense, we are just testing the routes. 

## _on the route_ `/`: 
- please send object `{'address': '77 main street town state 54321'}` 
- _along a `200` you will receive_ 
either `{'low': 10, 'high': 100, 'parcel': {a {big {complicated { object }}}}}`
- _or_ a `404`

## _on the route_ `/survey`
- please send the object {
    "countertops": "laminate",
	"flooring": "hardwood",
	"roofAge": "0-4 years",
	"furnaceAge": "0-4 years"
}
- _along a `200` you will receive_ `{'valuation': 'a string showing what
  you just sent'}`
  
  Sorry, this is supposed to be two keys `low` and `high`, I'll fix it in an
  hour or two or just wait until the statistics is done and we hand it to you
  with real statistics. 
