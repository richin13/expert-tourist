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
    (2, 'Culturales'),
)

def coords_to_gmaps_url(lat, long):
    return 'http://maps.google.co.cr/maps?q={},{}'.format(lat, long)
