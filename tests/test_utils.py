from expert_tourist.utils import gmaps_url_to_coords
from tests.tests import BaseTestConfig

class TestUtils(BaseTestConfig):
    def test_url_to_coords(self):
        url = 'http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035'
        lat, long = gmaps_url_to_coords(url)

        self.assertEqual(lat, 9.8757875656828)
        self.assertEqual(long, -84.03733452782035)
