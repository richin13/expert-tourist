from unittest import TestCase

from expert_tourist.utils import coords_to_gmaps_url


class TestUtils(TestCase):
    def test_url_to_coords(self):
        lat, long = 9.8757875656828, -84.03733452782035
        url = coords_to_gmaps_url(lat, long)

        self.assertEqual(url, 'http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035')
