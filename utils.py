from qgis.core import Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsMessageLog, QgsPointXY, QgsProject
from qgis.utils import iface


# noinspection PyBroadException
def point2wgs84(point: QgsPointXY):
    """
    Converts the coordinates of a point to WGS84

    :rtype: QgsPointXY
    :param point: A qgis.core.QgsPointXY object representing the point to convert
    :return: A qgis.core.QgsPointXY object representing the point in WGS84
    """
    try:
        crs = iface.mapCanvas().mapRenderer().destinationCrs()
    except:
        crs = iface.mapCanvas().mapSettings().destinationCrs()

    t = QgsCoordinateReferenceSystem()
    t.createFromSrid(4326)
    f = crs

    try:
        transformer = QgsCoordinateTransform(f, t)
    except:
        transformer = QgsCoordinateTransform(f, t, QgsProject.instance())
    try:
        pt: QgsPointXY = transformer.transform(point)
    except:
        pt: QgsPointXY = transformer.transform(QgsPointXY(point))
    return pt


def get_log_level(level):
    if level == 'info':
        lev = Qgis.Info
    elif level == 'warning':
        lev = Qgis.Warning
    elif level == 'critical':
        lev = Qgis.Critical
    elif level == 'success':
        lev = Qgis.Success
    else:
        lev = Qgis.Info
    return lev


def log_message(*msg, level: str = 'info'):
    """
    Writes a message to the QGIS message log

    :rtype: None
    :param msg: The message / parts of the message to write
    :param level: The level that the message should have.<br>Can be 'info', 'warning', 'critical', 'success' or None
    """
    message = ''
    for text in msg:
        message += '{0!s} '.format(text)
    QgsMessageLog.logMessage(message=message, level=get_log_level(level))


def message_bar(*msg, level: str = 'info'):
    """
    Creates a new qgis message bar

    :rtype: None
    :param msg: The message / parts of the message to write
    :param level: The level that the message should have.<br>Can be 'info', 'warning', 'critical', 'success' or None
    """
    message = ''
    for text in msg:
        message += '{0!s} '.format(text)
    iface.messageBar().pushMessage(text=message, level=get_log_level(level))


class LayerNotFoundError(BaseException):
    """An exception for a not-found layer"""
    pass


class FileNotFound(BaseException):
    """An exception for a not-found file"""
    pass
