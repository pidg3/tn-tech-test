from src.data_parser import make_soup, get_name, get_type, get_num_bedrooms, get_num_bathrooms, get_amenities

with open("tests/test_page.html") as test_html:
  soup = make_soup(test_html)

  def test_making_soup():
      assert soup != None

  def test_get_name():
    assert get_name(soup) == 'Birch Lodge 16, Newton Stewart'

  def test_get_type():
    assert get_type(soup) == 'Entire house'

  def test_get_num_bedrooms():
    assert get_num_bedrooms(soup) == 2

  def test_get_num_bathrooms():
    assert get_num_bathrooms(soup) == 1

  def test_get_amenities():
    assert get_amenities(soup) == [
      'Hair dryer',
      'Bed linen',
      'TV',
      'Heating',
      'Smoke alarm',
      'Carbon monoxide alarm',
      'Wifi',
      'Kitchen',
      'Microwave',
      'Refrigerator',
      'Dishwasher',
      'Oven',
      'Private entrance',
      'Patio or balcony',
      'Long-term stays allowed'
    ]
