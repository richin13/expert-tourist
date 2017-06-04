import yaml
from tests.tests import BaseTestConfig

from expert_tourist.models import Place, PlaceCategory

yaml_str = """
Parque Acuático Cascada de Fuego:
    type: Balneario / Piscina
    contact: ''
    phone_number: 2276-6080
    email: cascadadefuegoparqueacuatico@gmail.com
    facebook: ''
    region: Valle Central
    area: Montaña
    location: San José, Desamparados, Patarrá
    address: 2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra
    google_maps: http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035
    hours: 'Lun-Dom: 8:00 am-5:00 pm'
"""


class TestModels(BaseTestConfig):
    def test_place_from_yaml(self):
        parsed_yml = yaml.load(yaml_str)
        place, categories = Place.from_yml(parsed_yml)

        self.assertEqual(place.name, 'Parque Acuático Cascada de Fuego')
        self.assertEqual(place.contact, '')
        self.assertEqual(place.phone_number, '2276-6080')
        self.assertEqual(place.email, 'cascadadefuegoparqueacuatico@gmail.com')
        self.assertEqual(place.facebook, '')
        self.assertEqual(place.region, 'Valle Central')
        self.assertEqual(place.area, 'Montaña')
        self.assertEqual(place.location, 'San José, Desamparados, Patarrá')
        self.assertEqual(place.address, '2km sur de la iglesia de San Antonio de Desamparados, carretera a Patarra')
        self.assertEqual(place.google_maps, 'http://maps.google.co.cr/maps?q=9.8757875656828,-84.03733452782035')
        self.assertEqual(place.latitude, 9.8757875656828)
        self.assertEqual(place.longitude, -84.03733452782035)
        self.assertEqual(place.hours, 'Lun-Dom: 8:00 am-5:00 pm')

        for c in categories:
            self.assertEqual(c.name, 'Balneario / Piscina')

