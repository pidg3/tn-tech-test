from src.data_parser import make_soup, get_name, get_type, get_num_bedrooms, get_num_bathrooms

with open("tests/test_page.html") as test_html:
  soup = make_soup(test_html)

  def test_making_soup():
      assert soup != None

  def test_get_name():
    assert get_name(soup) == 'Fionn Gart'

  def test_get_type():
    assert get_type(soup) == 'Entire house'

  def test_get_num_bedrooms():
    assert get_num_bedrooms(soup) == 3

  def test_get_num_bathrooms():
    assert get_num_bathrooms(soup) == 2

  # def test_get_amenities():
    # TODO: thinking needed about how to structure the result