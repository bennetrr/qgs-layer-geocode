from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox
from qgis.core import QgsApplication

from .resources import *
from .layer_geocode_dialog import LayerGeocodeDialog
from .geocode import GeocodeTask
from .utils import message_bar


# DEBUG
# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)


class LayerGeocode:
    def __init__(self, iface):
        self.iface = iface

        self.actions = []
        self.menu = 'Layer Geocode'

        self.first_start = None

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    # noinspection PyPep8Naming
    def initGui(self):
        icon_path = ':/plugins/layer_geocode/icon.png'
        self.add_action(
            icon_path,
            text='Geocode Layer',
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                'Layer Geocode',
                action)
            self.iface.removeToolBarIcon(action)

    # noinspection PyMethodMayBeStatic
    def task_finished(self, state: bool, description: str, exception: object):
        if state:
            message_bar('Task successfully completed: {}'.format(description), level='success')
        else:
            if exception is None:
                message_bar('Task canceled by user: {}'.format(description), level='warning')
            else:
                message_bar('Task exited with an error: {}; {}'.format(description, exception), level='critical')
                raise exception

    def run(self):
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start:
            self.first_start = False
            # noinspection PyAttributeOutsideInit
            self.dlg = LayerGeocodeDialog()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            layer_box: QgsMapLayerComboBox = self.dlg.layer
            field_box: QgsFieldComboBox = self.dlg.field

            layer = layer_box.currentLayer()
            field_name = field_box.currentField()

            task = GeocodeTask(layer, field_name)
            task.finished_signal.connect(self.task_finished)
            QgsApplication.taskManager().addTask(task)
            message_bar('Die Aufgabe "Alle Adressen bestimmen" wurde gestartet.', level='info')
