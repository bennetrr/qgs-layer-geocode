import os
from qgis.PyQt import uic, QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'layer_geocode_dialog_base.ui'))


class LayerGeocodeDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(LayerGeocodeDialog, self).__init__(parent)
        self.setupUi(self)
