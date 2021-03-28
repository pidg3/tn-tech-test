# Tech Test

### Brief

Scrape property name, property type (e.g Apartment), number of bedrooms, bathrooms and list of the amenities for the following 3 properties:
- https://www.airbnb.co.uk/rooms/33571268
- https://www.airbnb.co.uk/rooms/33090114
- https://www.airbnb.co.uk/rooms/40558945

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
- [] Grab other fields (amenity list may be slightly tricker as full list in modal) and print
- [] Think about concurrency - we don't want to wait for pages to be loaded synchronously

Other ideas:

- [] Test to validate the page structure hasn't changed?
- [] Wrap everything in an API call (with caching?)
- [] Reverse engineering APIs - is this feasible? Might be a lot faster than scraping, particularly due to way content is loaded dynamically

### Reminders (tidy up before submitting)

- Need Firefox Selenium thing to run
- Refactoring 'elements to load' and div path