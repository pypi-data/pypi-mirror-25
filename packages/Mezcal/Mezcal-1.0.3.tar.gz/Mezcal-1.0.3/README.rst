Description
===========
Library for generating a set of color schemes from a provided color. Mezcal is a distilled from the awesome `Agave`_ color scheme generator application.
.. _Agave: http://home.gna.org/colorscheme/

Depends On
----------
1) python >= 3.4
2) numpy >= 1.12.1

Usage Example
-------------
.. code:: python
	from Mezcal.Barrel import Bottle

	glass = Bottle()

	# Set rgb, hsv, hex on Bottle objects.
	glass.rgb = ( 100, 200, 55 )


	# Get the corresponding color schemes.
	print( "RGB color scheme:")
	print( glass.rgb_scheme )

	print( "HSV color scheme")
	print( glass.hsv_scheme )

	print( "Hex color scheme")
	print( glass.hex_scheme )

	glass.hsv = ( 360, 100, 50 )
	print( glass.analogous[0].hex )

	# Define hex, rgb, hsv on class creation.
	glass = Bottle( hex="#0066cc" )
	print( glass.rgb_scheme )

Mezcal PyQt5 Visualization
--------------------------
.. code:: bash
	#!/bin/bash
	# Requires PyQt5 to be installed.
	python widget/SampleWidget.py
