#!/usr/bin/python
# coding=utf-8
"""
InaSAFE Disaster risk assessment tool developed by AusAid -
**CLI implementation for inasafe project.**

Contact : jannes@kartoza.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

    Note :
        cli: command line interface
    .. versionadded:: 3.2
"""
import logging
import os

from qgis.core import (
    QgsRasterLayer,
    QgsVectorLayer,
    QgsRectangle,
    QgsMapLayerRegistry,
    QgsCoordinateReferenceSystem)
from qgis.testing.mocked import get_iface

from docopt import docopt, DocoptExit


from safe.common.version import get_version
from safe.utilities.gis import qgis_version, validate_geo_array
from safe.utilities.osm_downloader import download
from safe.impact_function.impact_function import ImpactFunction
from safe.datastore.folder import Folder
from safe.definitions.constants import PREPARE_SUCCESS, ANALYSIS_SUCCESS
from safe.definitions.utilities import update_template_component
from safe.definitions.reports.components import (
    map_report,
    standard_impact_report_metadata_pdf)
from safe.report.impact_report import ImpactReport
from safe.report.report_metadata import ReportMetadata


__copyright__ = "Copyright 2016, The InaSAFE Project"
__license__ = "GPL version 3"
__email__ = "info@inasafe.org"
__revision__ = '$Format:%H$'

CURRENT_DIR = os.path.abspath(os.path.realpath(os.getcwd()))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
USAGE = file(os.path.join(PROJECT_ROOT, 'usage.txt')).read()
LOGGER = logging.getLogger('InaSAFE')
IFACE = get_iface()


class CommandLineArguments(object):
    """Instance objects class for shell arguments.
        .. versionadded:: 3.2
    """
    def __init__(self, arguments_=None):
        LOGGER.debug('CommandLineArguments')

        # Init members
        self._hazard_path = None
        self._exposure_path = None
        self._aggregation_path = None

        self.hazard_layer = None
        self.exposure_layer = None
        self.aggregation_layer = None
        self.output_dir = None
        self.extent = None
        self.exposure_type = None

        # other mode
        self.version = False
        self.download = False

        if not arguments_:
            return

        # Use setter for proper assignments
        if arguments_['--hazard']:
            self.hazard_path = arguments_['--hazard']

        if arguments_['--exposure']:
            self.exposure_path = arguments_['--exposure']

        if arguments_['--aggregation']:
            self.aggregation_path = arguments_['--aggregation']

        if arguments_['--extent']:
            self.extent = arguments_['--extent'].replace(',', '.').split(':')

        if arguments_['--output-dir']:
            self.output_dir = arguments_['--output-dir']

        # mode
        self.version = arguments_['--version']
        if arguments_['--download']:
            self.download = arguments_['--download']
            self.exposure_type = arguments_['--feature-type']

    @property
    def hazard_path(self):
        """Getter for the hazard path.

        :return: The path to hazard layer.
        :rtype: str
        """
        return self._hazard_path

    @hazard_path.setter
    def hazard_path(self, path):
        """Setter for hazard path.

        :param path: The full path to the layer.
        :type path:str
        """
        self._hazard_path = path
        self.hazard_layer = get_layer(self._hazard_path, 'Hazard Layer')

    @property
    def exposure_path(self):
        """Getter for the exposure path.

        :return: The path to exposure layer.
        :rtype: str
        """
        return self._exposure_path

    @exposure_path.setter
    def exposure_path(self, path):
        """Setter for exposure path.

        :param path: The full path to the layer.
        :type path:str
        """
        self._exposure_path = path
        self.exposure_layer = get_layer(self._exposure_path, 'Exposure Layer')

    @property
    def aggregation_path(self):
        """Getter for the aggregation path.

        :return: The path to aggregation layer.
        :rtype: str
        """
        return self._aggregation_path

    @aggregation_path.setter
    def aggregation_path(self, path):
        """Setter for exposure path.

        :param path: The full path to the layer.
        :type path:str
        """
        self._aggregation_path = path
        self.aggregation_layer = get_layer(
            self._aggregation_path, 'Hazard Layer')


def download_exposure(cli_arguments):
    """Download OSM resources.

        Download layers from OSM within the download extent.

        This function might generate a popup.
        .. versionadded:: 3.2

    :param cli_arguments:  User inputs.
    :type cli_arguments: CommandLineArguments
    """
    extent = [
        float(cli_arguments.extent[0]),
        float(cli_arguments.extent[1]),
        float(cli_arguments.extent[2]),
        float(cli_arguments.extent[3])
        ]

    if not os.path.exists(cli_arguments.output_dir):
        os.makedirs(cli_arguments.output_dir)

    download_path = os.path.join(
        cli_arguments.output_dir, cli_arguments.exposure_type)
    if validate_geo_array(extent):
        download(
            cli_arguments.exposure_type,
            download_path,
            extent)
        if os.path.exists(download_path + '.shp'):
            download_path += '.shp'
            cli_arguments.exposure_path = download_path
            print 'Download successful'
            print 'Output: ' + cli_arguments.exposure_path
    else:
        print 'Exposure download extent is invalid'
        print str(extent)


def join_if_relative(path_argument):
    """Make path absolute.

    .. versionadded:: 3.2

    :param path_argument: Absolute or relative path to a file.
    :type path_argument: str

    :returns: Absolute path to file.
    :rtype: str
    """
    if not os.path.isabs(path_argument):
        return os.path.join(CURRENT_DIR, path_argument)
    else:
        return os.path.abspath(path_argument)


def get_layer(layer_path, layer_base=None):
    """Get layer from path.

    .. versionadded:: 3.3

    :param layer_path: layer full name
    :type layer_path: str

    :param layer_base: layer base name (title)
    :type layer_base: str

    :returns: Vector or Raster layer depending on input arguments.
    :rtype: QgsVectorLayer, QgsRasterLayer

    :raises: Exception
    """
    layer = None
    try:
        layer_path = join_if_relative(layer_path)
        basename, ext = os.path.splitext(os.path.basename(layer_path))
        if not layer_base:
            layer_base = basename

        if os.path.exists(layer_path):
            if ext in ['.shp', '.geojson', '.gpkg']:
                layer = QgsVectorLayer(layer_path, layer_base, 'ogr')
            elif ext in ['.asc', '.tif', '.tiff']:
                layer = QgsRasterLayer(layer_path, layer_base)
            else:
                print "Unknown layer's filetype " + layer_base

        if layer is None or not layer.isValid():
            print "Layer %s is NOT VALID" % layer_path

        return layer
    except Exception as exception:
        print exception.message
        print exception.__doc__


def run_impact_function(cli_arguments):
    """Runs an analysis and delegates producing pdf and .geojson output layers.

    .. versionadded:: 3.2

    :param cli_arguments: User inputs.
    :type cli_arguments: CommandLineArguments
    """
    # Set up impact function
    impact_function = ImpactFunction()
    impact_function.hazard = cli_arguments.hazard_layer
    impact_function.exposure = cli_arguments.exposure_layer
    impact_function.aggregation = cli_arguments.aggregation_layer
    # Set the datastore
    if not os.path.exists(cli_arguments.output_dir):
        os.makedirs(cli_arguments.output_dir)
    impact_function.datastore = Folder(cli_arguments.output_dir)
    impact_function.datastore.default_vector_format = 'geojson'

    # Set the extent
    if cli_arguments.extent:
        impact_function.requested_extent_crs = \
            QgsCoordinateReferenceSystem(4326)
        try:
            impact_function.requested_extent = QgsRectangle(
                float(cli_arguments.extent[0]),
                float(cli_arguments.extent[1]),
                float(cli_arguments.extent[2]),
                float(cli_arguments.extent[3])
            )
        except AttributeError:
            print "Extent is not valid..."
            pass

    # Prepare impact function
    status, message = impact_function.prepare()
    if status != PREPARE_SUCCESS:
        print message.to_text()
        return status, message, None

    status, message = impact_function.run()
    if status != ANALYSIS_SUCCESS:
        print message.to_text()
        return status, message, None

    return status, message, impact_function


def generate_impact_map_report(cli_arguments, impact_function, iface):
    """Generate impact map pdf from impact function.

    :param cli_arguments: User inputs.
    :type cli_arguments: CommandLineArguments

    :param impact_function: The impact function used.
    :type impact_function: ImpactFunction

    :param iface: QGIS QGisAppInterface instance.
    :type iface: QGisAppInterface

    .. versionadded:: 4.0
    """
    layers = [cli_arguments.hazard_layer, cli_arguments.exposure_layer]
    if cli_arguments.aggregation_layer:
        layers.append(cli_arguments.aggregation_layer)
    layer_registry = QgsMapLayerRegistry.instance()
    layer_registry.addMapLayers(layers)
    layer_registry.addMapLayers(impact_function.outputs)

    # create impact report instance
    report_metadata = ReportMetadata(
        metadata_dict=update_template_component(map_report)
    )
    impact_report = ImpactReport(
        iface,
        report_metadata,
        impact_function=impact_function)
    # get the extent of impact layer
    impact_report.qgis_composition_context.extent = \
        impact_function.impact.extent()
    # set the ouput folder
    impact_report.output_folder = cli_arguments.output_dir

    return impact_report.process_components()


def generate_impact_report(cli_arguments, impact_function, iface):
    """Generate the impact report from an impact function.

    :param cli_arguments: User inputs.
    :type cli_arguments: CommandLineArguments

    :param impact_function: The impact function used.
    :type impact_function: ImpactFunction

    :param iface: QGIS QGisAppInterface instance.
    :type iface: QGisAppInterface

    .. versionadded:: 4.0

    """
    # create impact report instance
    report_metadata = ReportMetadata(
        metadata_dict=standard_impact_report_metadata_pdf)
    impact_report = ImpactReport(
        iface,
        report_metadata,
        impact_function=impact_function)
    impact_report.output_folder = cli_arguments.output_dir

    return impact_report.process_components()


def build_report(cli_arguments, impact_function):
    """Produces pdf products.

        To be called after output files have been written into
        arguments.output_dir.

    .. versionadded:: 3.2

    :param cli_arguments: User inputs.
    :type cli_arguments: CommandLineArguments

    :param impact_function: The impact function used.
    :type impact_function: ImpactFunction

    :raises: Exception
    """
    LOGGER.info('Building a report')
    # Generate map report
    status, message = generate_impact_map_report(
        cli_arguments, impact_function, IFACE)
    if status != ImpactReport.REPORT_GENERATION_SUCCESS:
        raise Exception(message.to_text())

    # Generate table report
    status, message = generate_impact_report(
        cli_arguments, impact_function, IFACE)
    if status != ImpactReport.REPORT_GENERATION_SUCCESS:
        raise Exception(message.to_text())

    return status, message


def main():
    """Main function here."""
    try:
        shell_arguments = docopt(USAGE)
    except DocoptExit as exc:
        print exc.message
        return

    try:
        args = CommandLineArguments(shell_arguments)
        LOGGER.debug(shell_arguments)
        # Version
        if args.version is True:
            print 'QGIS VERSION: %s' % str(qgis_version()).replace('0', '.')
            print 'InaSAFE VERSION: %s' % get_version()

        # User is only interested in doing a download
        elif args.download and not args.hazard_path:
            print "Downloading..."
            download_exposure(args)

        # Interested in running a scenario
        elif args.hazard_path and args.exposure_path and args.output_dir:
            if not args.hazard_layer:
                return

            if not args.exposure_layer:
                return

            # if using aggregation make sure it's valid
            if args.aggregation_path and not args.exposure_layer:
                return

            status, msg, impact_function = run_impact_function(args)
            if status != ANALYSIS_SUCCESS:
                print 'Failed running impact function...'
                print msg
            else:
                print 'Running impact function is succesfull...'
                print 'Building reports...'
                status, msg = build_report(args, impact_function)
                if status != ImpactReport.REPORT_GENERATION_SUCCESS:
                    print 'Failed building reports...'
                    print msg
        else:
            print "Argument combination not recognised"
    except Exception as excp:
        print excp.message
        print excp.__doc__


if __name__ == '__main__':
    main()
