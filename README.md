# QGIS-Layer-Geocode
This plugin geocodes a whole layer using the OSM Nominatim API.

## Download
You can download the zip-file here: https://github.com/bennetrr/QGIS-Layer-Geocode/releases

## Usage
The icon is at this time the default icon for a nev plugin, a green power plug on yellow background (it will be changed later: [#1](https://github.com/bennetrr/QGIS-Layer-Geocode/issues/1)). You can find it in the _Plugins_ menu and in the toolbar. When you open it, you will see a form where you can select a layer and a field.

The layer needs to have a geometry that has excact one point (e.g. a point layer).

The field has to be a exsisting `String` field. You have to create it by your own, the plugin does not do that. You can name it how you want.

When you press _OK_, the plugin will send the coordinates of every point in the layer to [Nominatim](https://nominatim.org/), an open source address search API from OpenStreetMap. The result will be saved in the given field. Depending on the count points in your layer it takes realy long. Therefore you can see the progress in the status bar in QGIS.
