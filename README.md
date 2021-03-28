# Tech Test

### Brief

Scrape property name, property type (e.g Apartment), number of bedrooms, bathrooms and list of the amenities for the following 3 properties:
- https://www.airbnb.co.uk/rooms/33571268
- https://www.airbnb.co.uk/rooms/33090114
- https://www.airbnb.co.uk/rooms/40558945

### How to run

This little scraper logs out details to the console for the three properties (note - one of them doesn't exist, this is handled sensibly). 

- Make sure the following packages are installed in your python env: `requests pytest selenium bs4 pep8` (if using conda/miniconda you can create a new environment from the `environment.yml` file: `conda env create -f environment.yml`)
- Add the appropriate Firefox `geckodriver` file to your Python PATH as per instructions here: https://selenium-python.readthedocs.io/installation.html#drivers (this is needed for Selenium to work)
- That should be it!
  - `python main.py` to run the code.
  - `pytest` to run tests. 

### Next steps if @ work

- Is Selenium the right solution for this? It feels a bit slow and clunky. I'd want to discuss with people who are more experienced in scraping. A creative alternative might be to reverse engineer the APIs that are providing the data. A brief exercise to grep out the responses suggested there might be some mileage in this: try running `curl_demo.sh`.
- Refactor: both `data_parser` and `html_loader` are relying on the same elements. Splitting in this way is logical, but some sort of shared data structure describing the elements needed would help reduce duplication.
- Testing: I'd like to write a test to validate the page structure on Airbnb hasn't changed (sort of like a contract test).
- Concurrency: pages should be downloaded in parallel. 
- Docker: its a bit of a pain to have to set up the environment and download the Firefox driver. Would be better to create a new Docker image to automate this. 

Apart from that, it would depend on how this tool was to be used. Maybe we'd want a little API to be written in Flask to grab the odd property now and then? Or maybe it would be part of a bulk collection exercise - in which case we'd need to think about various things:
- Architecture - perhaps running via Lambdas would be a nice way of parallelising it.
- Validation of data collected. 
- How/where to store the data (would probably lend itself to DynamoDB or other document store).


### Plan

(Thought it would be worth including my train of thought as I went through this - see sub bullets)

Basic version:

- [x] Decide on scraper to use (looks like content loaded dynamically)
  - *Tried out Beautiful Soup - didn't work due to dynamic content, as expected.*
  - *However the parser seems nice. Let's try using Selenium to fully load the page, and then pass to Beautiful Soup to grab the actual data.*
- [x] Hack together basic scraper to grab property name and print to console
- [x] Structure things properly and add tests
  - *3rd property does not exist - handling needed!*
  - *Saving the HTML speeds things up a lot. Of course, risk is here these tests give us false confidence - the page structure could change at any moment.*
- [x] Grab other fields (amenity list may be slightly tricker as full list in modal) and print
  - *Couple of gotchas with amenities - struck through ones, and those with sub-text.*
  - *Assumed here the sub-text isn't needed, nor is the categorisation.*
