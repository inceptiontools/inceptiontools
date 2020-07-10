"""
    test_main
    ~~~~~~~~~

    Unit test cases for the :py:mod:`pyincept.main` module.
"""

__author__ = 'Andrew van Herick'
__copyright__ = \
    'Unpublished Copyright (c) 2020 Andrew van Herick. All Rights Reserved.'
__license__ = 'Apache Software License 2.0'

import logging
import os
import shutil
from contextlib import closing
from datetime import datetime
from io import StringIO
from logging import StreamHandler
from unittest import mock

from click.testing import CliRunner
from hamcrest import assert_that, contains_string, is_, starts_with

from pyincept import main
from tests.pyincept_test_base import PyinceptTestBase


class TestMain(PyinceptTestBase):
    """
    Unit test for class :py:mod:`pyincept`.
    """

    ##############################
    # Class attributes

    # See superclass declaration to understand the use of this attribute.
    _OVERWRITE_EXPECTED_FILE = False

    _PACKAGE_NAME = 'some_package_name'
    _AUTHOR = 'some_author'
    _AUTHOR_EMAIL = 'some_author_email'

    # Something earlier than the current year.
    _DATE = datetime(2000, 1, 1)

    ##############################
    # Class / static methods

    @classmethod
    def _get_resource_path(cls, resource_name):
        return os.path.abspath(
            os.path.join(
                __file__,
                os.pardir,
                '_resources',
                'test_pyincept',
                resource_name
            )
        )

    ##############################
    # Instance methods

    # Instance set up / tear down

    @mock.patch('pyincept.main.datetime')
    def setup(self, mock_datetime):
        """
        Called before each method in this class with a name of the form
        test_*().
        """
        mock_datetime.now.return_value = self._DATE

        # The project root directory should not already exist.  If it does,
        # something unexpected has happened, so raise.
        self._validate_path_doesnt_exist(self._PACKAGE_NAME)

        self._runner = CliRunner()
        self._result = self._runner.invoke(
            main.main,
            (self._PACKAGE_NAME, self._AUTHOR, self._AUTHOR_EMAIL)
        )

    def teardown(self):
        """
        Called after each method in this class with a name of the form
        test_*().
        """
        if os.path.exists(self._PACKAGE_NAME):
            shutil.rmtree(self._PACKAGE_NAME)

        self._validate_path_doesnt_exist(self._PACKAGE_NAME)

    # Test cases

    def test_main_maps_project_root(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = self._PACKAGE_NAME
        assert_that(
            os.path.isdir(dir_path),
            'Directory not found: {}'.format(dir_path)
        )

    def test_main_maps_package_name(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = 'Package distribution file for the {} library.'.format(
            self._PACKAGE_NAME
        )
        assert_that(content, contains_string(substring))

    def test_main_maps_author_name(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = "author='{}'".format(self._AUTHOR)
        assert_that(content, contains_string(substring))

    def test_main_maps_author_email(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = "author_email='{}'".format(self._AUTHOR_EMAIL)
        assert_that(content, contains_string(substring))

    def test_main_maps_date(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = 'Copyright (c) {}'.format(self._DATE.year)
        assert_that(content, contains_string(substring))

    def test_main_leaves_exit_status_0_on_success(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        assert_that(self._result.exit_code, is_(0))

    @mock.patch('pyincept.main._main')
    def test_main_leaves_exit_status_1_on_unhandled_error(self, mock__main):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        mock__main.side_effect = ValueError('Some test exception.')

        result = self._runner.invoke(
            main.main,
            (self._PACKAGE_NAME, self._AUTHOR, self._AUTHOR_EMAIL)
        )

        assert_that(result.exit_code, is_(1))

    @mock.patch('pyincept.main._logger')
    @mock.patch('pyincept.main._main')
    def test_main_logs_unhandled_errors(self, mock__main, mock__logger):
        """
        Unit test case for :py:method:`pyincept.main`.
        """

        mock__main.side_effect = ValueError('Some test exception.')

        with closing(StringIO()) as sio:
            stream_handler = StreamHandler(sio)
            logger = logging.getLogger('test_pyincept_mock_logger')
            logger.addHandler(stream_handler)
            mock__logger.return_value = logger
            self._runner.invoke(
                main.main,
                (self._PACKAGE_NAME, self._AUTHOR, self._AUTHOR_EMAIL)
            )

            actual = sio.getvalue()

        expected = 'Unexpected exception: package_name=some_package_name, ' \
                   'author=some_author, author_email=some_author_email\n'

        assert_that(actual, starts_with(expected))
