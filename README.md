# Tech Test

### Brief

Scrape property name, property type (e.g Apartment), number of bedrooms, bathrooms and list of the amenities for the following 3 properties:
- https://www.airbnb.co.uk/rooms/33571268
- https://www.airbnb.co.uk/rooms/33090114
- https://www.airbnb.co.uk/rooms/40558945

### Plan

Basic version:

- [] Decide on scraper to use (looks like content loaded dynamically)
- [] Hack together basic scraper to grab property name and print to console
- [] Structure things properly and add tests
- [] Grab other fields (amenity list may be slightly tricker as full list in modal) and print
- [] Think about concurrency - we don't want to wait for pages to be loaded synchronously

Other ideas:

- [] Test to validate the page structure hasn't changed?
- [] Wrap everything in an API call (with caching?)
- [] Reverse engineering APIs - is this feasible? Might be a lot faster than scraping, particularly due to way content is loaded dynamically
