# Route encodings

PRICE_ENCODING = (
    (0, 'Gratis'),
    (1, 'Barato'),
    (2, 'Moderado'),
    (3, 'Caro'),
)

AREA_ENCODING = (
    (0, 'Montaña'),
    (1, 'Rural'),
    (2, 'Ciudad'),
    (3, 'Costa'),
)

# Tourist encodings

VEHICLE_ENCODINGS = (
    (0, 'Todo terreno'),
    (1, 'Automóvil'),
    (2, 'Sin vehículo'),
)

BUDGET_ENCODING = (
    (0, 'Bajo'),
    (1, 'Medio'),
    (2, 'Alto'),
)

TRAVEL_DIST_ENCODING = (
    (0, 'Corta'),
    (1, 'Media'),
    (2, 'Larga'),
)

ACTIVITIES_ENCODING = (
    (0, 'Familiares'),
    (1, 'Aventuras'),
    (2, 'Casuales'),
)

# Classes encoding
# For the purpose of the homework, there are 3 classes. It will change in the future!
CLASSES_ENCODING = (
    (0, 'c1'),
    (1, 'c2'),
    (2, 'c3'),
)

def coords_to_gmaps_url(lat, long):
    return 'http://maps.google.co.cr/maps?q={},{}'.format(lat, long)

def convert_coordinates_to_point(coords):
    return {
        'x': coords[0],
        'y': coords[1]
    }

def convert_point_to_coordinates(point):
    return [point['x'], point['y']]