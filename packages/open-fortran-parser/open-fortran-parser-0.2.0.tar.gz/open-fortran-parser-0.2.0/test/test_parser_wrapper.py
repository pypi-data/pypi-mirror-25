"""Tests for parser_wrapper module."""

import logging
import pathlib
import unittest

from open_fortran_parser.parser_wrapper import execute_parser, parse

_LOG = logging.getLogger(__name__)

_HERE = pathlib.Path(__file__).resolve().parent

INPUT_PATHS = list(_HERE.joinpath('examples').glob('**/*.*'))
OUTPUT_PATHS = ['/tmp/out.xml', None]
VERBOSITIES = (0, 20, 80, 100)


class Tests(unittest.TestCase):

    maxDiff = None

    def test_execute_parser(self):
        output_path = OUTPUT_PATHS[0]
        for input_path in INPUT_PATHS:
            for verbosity in VERBOSITIES:
                with self.subTest(input_path=input_path, verbosity=verbosity):
                    execute_parser(input_path, output_path, verbosity)

    def test_generate_xml(self):
        transformations_path = _HERE.joinpath('transformations')
        transformations_path.mkdir(exist_ok=True)
        for input_path in INPUT_PATHS:
            for verbosity in VERBOSITIES:
                with self.subTest(input_path=input_path, verbosity=verbosity):
                    output_path = transformations_path.joinpath(input_path.name + '.xml')
                    root_node = execute_parser(input_path, output_path, verbosity)
                    self.assertIsNotNone(root_node)
                    self.assertTrue(output_path.exists())

    def test_execute_parser_stdout(self):
        for input_path in INPUT_PATHS:
            for output_path in OUTPUT_PATHS:
                for verbosity in VERBOSITIES:
                    with self.subTest(input_path=input_path, output_path=output_path,
                                      verbosity=verbosity):
                        execute_parser(input_path, output_path, verbosity)

    def test_parse(self):
        for input_path in INPUT_PATHS:
            for verbosity in VERBOSITIES:
                with self.subTest(input_path=input_path, verbosity=verbosity):
                    root_node = parse(input_path, verbosity)
                    self.assertIsNotNone(root_node)
                    self.assertEqual(root_node.tag, 'ofp')
                    self.assertEqual(len(root_node), 1)
                    file_node = root_node[0]
                    self.assertEqual(file_node.tag, 'file')
                    self.assertGreater(len(file_node), 0)
