# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    from .layer_geocode import LayerGeocode
    return LayerGeocode(iface)
