# Tech Test

## Brief

Scrape property name, property type (e.g Apartment), number of bedrooms, bathrooms and list of the amenities for the following 3 properties:
- https://www.airbnb.co.uk/rooms/33571268
- https://www.airbnb.co.uk/rooms/33090114
- https://www.airbnb.co.uk/rooms/40558945

## Overview

- Exposes an endpoint `http://127.0.0.1:5000/v1/properties/[comma separated property IDs]` using Flask.
- Uses Selenium to navigate the page and wait for elements to load.
- Runs multiple Selenium sessions in parallel using threads (reduces time to get the three properties from about 25 to 12 seconds). 
- Handles missing properties and regex issues. 
- Returns time taken. 

Once the app is running (see below), to get data for the three requested properties using curl: `curl http://127.0.0.1:5000/v1/properties/33571268,33090114,40558945`. This should return:

```
{
  "metadata": {
    "timeTaken": 11.464621543884277
  },
  "results": [
    {
      "amenities": [
        "Dryer",
        "Washing machine",
        "Cable TV",
        "TV",
        "Wifi",
        "Microwave",
        "Dishwasher",
        "Garden or backyard",
        "Long-term stays allowed"
      ],
      "name": "Fionn Gart",
      "numBathrooms": 2,
      "numBedrooms": 3,
      "propertyType": "Entire house",
      "success": true,
      "url": "https://www.airbnb.co.uk/rooms/33571268"
    },
    {
      "errorReason": "Timed out - property probably doesn't exist",
      "success": false,
      "url": "https://www.airbnb.co.uk/rooms/40558945"
    },
    {
      "amenities": [
        "Hair dryer",
        "Bed linen",
        "TV",
        "Heating",
        "Smoke alarm",
        "Carbon monoxide alarm",
        "Wifi",
        "Kitchen",
        "Microwave",
        "Refrigerator",
        "Dishwasher",
        "Oven",
        "Private entrance",
        "Patio or balcony",
        "Long-term stays allowed"
      ],
      "name": "Birch Lodge 16, Newton Stewart",
      "numBathrooms": 1,
      "numBedrooms": 2,
      "propertyType": "Entire house",
      "success": true,
      "url": "https://www.airbnb.co.uk/rooms/33090114"
    }
  ]
}
```

## How to run

- Make sure the following packages are installed in your python env: `requests flask pytest selenium bs4 pep8` (if using conda/miniconda you can create a new environment from the `environment.yml` file: `conda env create -f environment.yml`)
- Add the appropriate Firefox `geckodriver` file to your Python PATH as per instructions here: https://selenium-python.readthedocs.io/installation.html#drivers (this is needed for Selenium to work)
- To get the server running:
  - `export FLASK_APP=main.py`
  - `python -m flask run`
  - Now the endpoint can be pinged as described above. 
- To run the tests:
  - `pytest`

## Next steps if @ work

- Is Selenium the right solution for this? It feels a bit slow and clunky. I'd want to discuss with people who are more experienced in scraping. 
- A creative alternative might be to reverse engineer the APIs that are providing the data. I got this half working, but keys seem to rotate quite frequently. Probably do-able but not trivial. 
- Refactor: both `data_parser` and `html_loader` are relying on the same DOM elements. Splitting in this way is logical, but some sort of shared data structure describing the elements needed would help reduce duplication.
- Another refactor: speed up detecting a property does not exist. Currently just waiting for Selenium waits to time out. 
- Testing: I'd like to write a test to validate the page structure on Airbnb hasn't changed (sort of like a contract test). Also, Flask API could probably use a test or two. 
- Docker: its a bit of a pain to have to set up the environment and download the Firefox driver. Would be better to create a new Docker image to automate this. 

Apart from that, it would depend on how this tool was to be used. Given it takes quite a while to load (and is a bit flaky, with multiple attempts sometimes needed) it would lend itself to some sort of queue/worker system. Perhaps using SQS/Lambdas on AWS, putting the results in DynamoDB. We'd probably also want some sort of continuous validation of the data collected.

If it is for one-off requests here and there, I'd suggest a simple caching system would be in order, assuming the same properties will be queried regularly. 

## Assumptions

- We don't need the categories of amenity (e.g. 'Bedroom and laundry'), nor the sub-text (e.g. 'Space where guests can cook their own meals' for Kitchen)
- Property type = the text before 'hosted by TravelNest' (e.g. 'Entire house')
