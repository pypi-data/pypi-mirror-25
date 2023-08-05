# coding=utf-8
__author__ = 'Jannes123'
__project_name__ = 'inasafe'
__filename__ = 'test_inasafe.py'
__date__ = '01/06/15'
__copyright__ = 'jannes@kartoza.com'

# Hackaround for travis
import sys
if not hasattr(sys, 'argv'):
    sys.argv = ['']

import unittest
import shutil
import os
from tempfile import mkdtemp
from contextlib import contextmanager
from StringIO import StringIO

import safe
from inasafe import (
    main,
    download_exposure,
    run_impact_function,
    build_report,
    CommandLineArguments,
    ImpactReport,
    ANALYSIS_SUCCESS,
    USAGE)

from PyQt4.QtCore import QDir


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def setup_args(args_dict):
    """Prepares args for test."""
    args = CommandLineArguments(args_dict)
    args.output_dir = os.path.join(
            QDir(mkdtemp()).absolutePath(), args.output_dir)
    os.makedirs(args.output_dir)
    return args


def remove_test_dir(output_dir):
    """Remove test directory."""
    if os.path.exists(output_dir):
        shutil.rmtree(os.path.join(output_dir, os.pardir), ignore_errors=True)


class TestInasafeCommandLine(unittest.TestCase):
    """Test Module for inasafe command line client.
            run from safe/ directory
    """
    def setUp(self):
        self.safe_dir_path = os.path.dirname(safe.__file__)
        # 1. Args with no aggregation
        self.args_no_aggregation = setup_args({
            '--download': False,
            '--hazard': os.path.join(
                self.safe_dir_path, 'test', 'data', 'gisv4', 'hazard',
                'tsunami_vector.geojson'),
            '--exposure':
                os.path.join(
                    self.safe_dir_path, 'test', 'data', 'gisv4', 'exposure',
                    'raster', 'population.asc'),
            '--aggregation': None,
            '--extent': '106,7999364:-6,2085970:106,8525945:-6,1676174',
            '--output-dir': 'test_cli',
            '--version': False})

        # 2. Args with aggregation
        self.args_with_aggregation = setup_args({
            '--download': False,
            '--hazard': os.path.join(
                self.safe_dir_path, 'test', 'data', 'gisv4', 'hazard',
                'tsunami_vector.geojson'),
            '--exposure':
                os.path.join(
                    self.safe_dir_path, 'test', 'data', 'gisv4', 'exposure',
                    'raster', 'population.asc'),
            '--aggregation': os.path.join(
                self.safe_dir_path, 'test', 'data', 'gisv4', 'aggregation',
                'small_grid.geojson'),
            '--extent': None,
            '--output-dir': 'test_cli',
            '--version': False})

        # 3. Args for download
        self.args_download = setup_args({
            '--aggregation': None,
            '--download': True,
            '--exposure': None,
            '--extent': '106,85:-6,2085970:106,8525945:-6,20',
            '--hazard': None,
            '--help': False,
            '--feature-type': 'buildings',
            '--output-dir': 'test_cli',
            '--version': False})

    def test_main(self):
        """Test basic command."""
        # Hackaround argv not defined on travis
        import sys
        if not hasattr(sys, 'argv'):
            sys.argv = ['']

        with captured_output() as (out, err):
            main()
        output = out.getvalue().strip()
        self.assertIn(output, USAGE)

    def test_download(self):
        """Test download using CLI"""
        download_exposure(self.args_download)
        self.assertTrue(os.path.exists(self.args_download.exposure_path))

    def test_run_impact_function_no_aggregation(self):
        """Test whether we can run impact function with no aggregation."""
        status, message, impact_function = run_impact_function(
            self.args_no_aggregation)
        self.assertEqual(status, ANALYSIS_SUCCESS)
        # There should be 2 files for each layer (.geojson, and .xml)
        self.assertEqual(
            2 * len(impact_function.datastore.layers()),
            len(os.listdir(self.args_no_aggregation.output_dir)))

    def test_run_impact_function_with_aggregation(self):
        """Test whether we can run impact function with aggregation."""
        status, message, impact_function = run_impact_function(
            self.args_with_aggregation)
        self.assertEqual(status, ANALYSIS_SUCCESS)

    def test_build_report(self):
        """Test whether a pdf can be created from
            run_impact_function's product.
        """
        status, message, impact_function = run_impact_function(self.args_no_aggregation)
        self.assertEqual(status, ANALYSIS_SUCCESS)

        status, message = build_report(self.args_no_aggregation, impact_function)
        self.assertEqual(status, ImpactReport.REPORT_GENERATION_SUCCESS)

    def tearDown(self):
        # remove output dir
        remove_test_dir(self.args_no_aggregation.output_dir)
        remove_test_dir(self.args_with_aggregation.output_dir)
        remove_test_dir(self.args_download.output_dir)
