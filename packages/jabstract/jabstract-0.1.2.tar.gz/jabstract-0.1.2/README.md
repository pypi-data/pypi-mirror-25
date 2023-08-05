[![Build Status](https://travis-ci.org/internap/jabstract.svg?branch=master)](https://travis-ci.org/internap/jabstract)

# Welcome unit testers!

## That's not cool:

```
def test_something():
    api_response = {
        "field1": "value1",
        "field2": "value2",
        ....
        "field37": "value37",
        ....
        "field7632": "value7632"
    }

    myapi.return_value = api_response
    
    result = production_code()
    
    assert result == "value37"
```

^ This is annoying if your `production_code` method only uses field37 right?

Of course you could only define the field37 in your test but if a log or something else irrelevant to THIS test uses another field, it has to be there even if it's irrelevant to THIS test.

## That's prettier:


```
api_response = jabstract({
    "field1": "value1",
    "field2": "value2",
    ....
    "field37": "value37",
    ....
    "field7632": "value7632"
})

def test_something():
    myapi.return_value = api_response(field37="value37")
    
    result = production_code()
    
    assert result == "value37"
```

^ The test is so much more beautiful!

# USAGE

Declare your json responses somewhere:

```
from jabstract import jabstract

api_response = jabstract({
    ... json-ish payload ...
})
```

Then use it in your tests by defining only relevant fields:

```
.return_value = api_response(
   key=value
)
```

It even supports complex payloads!

```
api_response = jabstract({
    "client": {
        "name": "John doe",
        "email": "johndoe@example.org"
    }
})

.return_value = api_response(
   client=dict(name="Foobar")
)
```

\* note that `response["client"]["email"]` will keep its default value.

# Best practices

Tests using jabstracted payload should define only what is relevant to the test, not less, not more, so that it is obvious to the human eye where a value come from

let's test this code
```
def name_getter(payload):
    return payload["client"]["name"]
```

## **Good** example:
```
api_response = jabstract({
    "client": {
        "name": "John doe",
        "email": "johndoe@example.org"
    }
})

def test_name_getter():
    payload = api_response(client=dict(name="Baboon 2.0"))

    assert name_getter(payload) == "Baboon 2.0"
```

**Reviewer says** : Ohhh so it takes the name of the client from the payload... +2

## ~~BAD~~ example

```
api_response = jabstract({
    "client": {
        "name": "John doe",
        "email": "johndoe@example.org"
    }
})

def test_name_getter():
    payload = api_response()
    
    assert name_getter(payload) == "John doe"
```

**Reviewer says** : Who the hell is john doe... click on payload... ahhh i see... meh, +1
