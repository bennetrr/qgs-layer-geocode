import json
import urllib.request

from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsFeature, QgsProject, QgsTask, QgsVectorLayer

from .utils import LayerNotFoundError, point2wgs84


class GeocodeTask(QgsTask):
    finished_signal = pyqtSignal(bool, str, object)

    def __init__(self, layer: QgsVectorLayer, fiel_name: str):
        super().__init__('Layer Geocoding of "{}"'.format(layer.name()), QgsTask.CanCancel)

        self.exception = None
        self.layer = layer
        self.field_name = fiel_name

        # Counters for progress display
        self.total_features = 0
        self.finished_features = 0

    def geocode_feature(self, feature: QgsFeature):

        # Get the coordinates of the point
        coord = feature.geometry().asPoint()
        coord_converted = point2wgs84(coord)
        lat = coord_converted[1]
        lon = coord_converted[0]

        # Send the coordinates to the osm api
        url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}'.format(lon=lon, lat=lat)
        con = urllib.request.urlopen(url)
        res = con.read().decode('utf-8')
        con.close()
        results = json.loads(res)

        result = results['display_name']

        # Save the address to the feature
        feature[self.field_name] = result
        self.layer.updateFeature(feature)

        self.finished_features += 1

    def run(self):
        try:
            self.total_features = self.layer.featureCount()

            self.layer.startEditing()
            for feature in self.layer.getFeatures():
                # Look if the task was cancelled
                if self.isCanceled():
                    self.finished_signal.emit(False, self.description(), self.exception)
                    return False

                self.geocode_feature(feature)

                # Display progress
                self.setProgress(self.finished_features / self.total_features * 100)
            self.layer.commitChanges()

            self.finished_signal.emit(True, self.description(), self.exception)
            return True
        except Exception as ex:
            self.exception = ex
            self.finished_signal.emit(False, self.description(), self.exception)
            return False
