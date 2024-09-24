# Perdix for QGIS

## About
Perdix is a [QGIS](http://www.qgis.org/en/site/) plugin forked from the "Space Syntax Toolkit" and offering user friendly space syntax analysis workflows in a GIS environment. It provides a front-end for the [depthmapX](https://varoudis.github.io/depthmapX/) software within QGIS, for seamless spatial network analysis. Furthermore, it includes tools for urban data management and analysis, namely land use, entrances, frontages, pedestrian movement, road centre lines, and service areas.

Originally developed by Jorge Gil at the Space Syntax Laboratory, The Bartlett, UCL, the plugin includes contributions from:
* [Space Syntax Limited](https://github.com/spacesyntax) - Ioanna Kovolou, Abhimanyu Acharya, Stephen Law, Laurens Versluis

## Installation
The plug-in can be installed from the QGIS Plugins Manager, and updates become automatically available once submitted to the QGIS plugins repository.

## Software Requirements
* QGIS (3.00 or above) - [http://www.qgis.org/en/site/](http://www.qgis.org/en/site/)
* depthmapXnet - [http://archtech.gr/varoudis/depthmapX/?dir=depthmapXnet](http://archtech.gr/varoudis/depthmapX/?dir=depthmapXnet)

## Support
If you need help using the toolkit in your space syntax research, you can send an e-mail to the mailing list (spacesyntax@jiscmail.ac.uk) for support from the space syntax community.
If you encounter problems when using the software, please check the [Wiki](https://github.com/SpaceGroupUCL/qgisSpaceSyntaxToolkit/wiki) and the [issues list](https://github.com/SpaceGroupUCL/qgisSpaceSyntaxToolkit/issues) for solutions.
For new problems, technical questions, or suggestions add the issue to the [issues list](https://github.com/SpaceGroupUCL/qgisSpaceSyntaxToolkit/issues).

## Where to find...
* The toolkit source code can be downloaded from the 'perdix' folder.
* Documentation can be obtained from the 'documents' folder.
* A sample dataset is in the 'data' folder, for experimenting with the plugin and following the documentation.

## Development notes:
* Development of this module has been done primarily using PyCharm, with the top folder (qgisSpaceSyntaxToolkit) selected and the QGIS python selected as an interpreter. This allows for having a similar module loading process as QGIS itself.
* Unit tests reside in the perdix/tests directory, but have to be carrie out from the top directory of the repository (qgisSpaceSyntaxToolkit).
