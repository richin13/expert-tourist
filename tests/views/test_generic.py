from . import TestViewCase


class TestGenericViews(TestViewCase):
    """Test case used to tests generic views like 404 error handling"""

    def test_non_existent_route(self):
        fake = self.fake
        url = '/api/{}'.format(fake.md5())

        res = self.app.get(
            url,
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 404)

    def test_json_decode_error(self):
        res = self.app.post(
            '/api/places',
            content_type='application/json',
            headers=self._authorize()
        )

        self.assertEqual(res.status_code, 400)
