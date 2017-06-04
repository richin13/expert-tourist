def gmaps_url_to_coords(url):
    gmaps_coords = url.split('=')
    coords = (0.0, 0.0) # defaults to 0,0
    if len(gmaps_coords) == 2:
        gmaps_coords = gmaps_coords[1]
        coords = tuple(map(lambda c: float(c), gmaps_coords.split(',')))

    return coords
