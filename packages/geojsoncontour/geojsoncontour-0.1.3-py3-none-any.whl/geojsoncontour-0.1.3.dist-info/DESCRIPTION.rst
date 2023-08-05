geojsoncontour
==============

| |Build Status| |PyPI version| |Coverage Status|
| A Python 3 module to convert matplotlib contour plots to geojson.

Designed to show geographical `contour
plots <http://matplotlib.org/examples/pylab_examples/contour_demo.html>`__,
created with
`matplotlib/pyplot <https://github.com/matplotlib/matplotlib>`__, as
vector layer on interactive slippy maps like
`OpenLayers <https://github.com/openlayers/ol3>`__ and
`Leaflet <https://github.com/Leaflet/Leaflet>`__.

Demo project that uses geojsoncontour:
`climatemaps.romgens.com <http://climatemaps.romgens.com>`__

Currently only supports contour lines.

Installation
------------

The recommended way to install is via pip,

::

    $ pip install geojsoncontour

Usage
-----

Contour plot to geojson
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import numpy
    import matplotlib.pyplot as plt
    import geojsoncontour

    # Create contour data lon_range, lat_range, Z
    <your code here>

    # Create a contour plot plot from grid (lat, lon) data
    figure = plt.figure()
    ax = figure.add_subplot(111)
    contour = ax.contour(lon_range, lat_range, Z, levels=levels, cmap=plt.cm.jet)

    # Convert matplotlib contour to geojson
    geojsoncontour.contour_to_geojson(
        contour=contour,
        geojson_filepath='out.geojson',
        contour_levels=levels,
        ndigits=3,
        unit='m'
    )

See `example1.py <geojsoncontour/examples/example1.py>`__ for a basic
but complete example.

Show the geojson on a map
~~~~~~~~~~~~~~~~~~~~~~~~~

An easy way to show the generated geojson on a map is the online geojson
renderer `geojson.io <http://geojson.io>`__.

Style properties
~~~~~~~~~~~~~~~~

Stroke color and width are set as geojson properties following
https://github.com/mapbox/simplestyle-spec.

Create geojson tiles
~~~~~~~~~~~~~~~~~~~~

Try `geojson-vt <https://github.com/mapbox/geojson-vt>`__ or
`tippecanoe <https://github.com/mapbox/tippecanoe>`__ if performance is
an issue and you need to tile your geojson contours.

Tests
-----

Run all tests,

::

    python -m unittest discover

.. |Build Status| image:: https://travis-ci.org/bartromgens/geojsoncontour.svg?branch=master
   :target: https://travis-ci.org/bartromgens/geojsoncontour
.. |PyPI version| image:: https://badge.fury.io/py/geojsoncontour.svg
   :target: https://badge.fury.io/py/geojsoncontour
.. |Coverage Status| image:: https://coveralls.io/repos/github/bartromgens/geojsoncontour/badge.svg?branch=master
   :target: https://coveralls.io/github/bartromgens/geojsoncontour?branch=master


