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

def coords_to_gmaps_url(lat, long):
    return 'http://maps.google.co.cr/maps?q={},{}'.format(lat, long)
