"""
file_renderer
~~~~~~~~~~~~~

Houses the declaration of :py:class:`FileRenderer` along with supporting
classes, functions, and attributes.
"""

__author__ = 'Andrew van Herick'
__copyright__ = \
    'Unpublished Copyright (c) 2020 Andrew van Herick. All Rights Reserved.'
__license__ = 'Apache Software License 2.0'

from abc import ABC, abstractmethod

from pyincept.archetype_parameters import ArchetypeParameters
from pyincept.constants import UNIMPLEMENTED_ABSTRACT_METHOD_ERROR


class FileRenderer(ABC):
    """
    This abstract base class determines the interfaces by which files built
    by this project should be rendered and saved.
    """

    def path(self, root_dir: str, params: ArchetypeParameters) -> str:
        """
        Returns the full path (possibly non-absolute) to the file that will
        be saved by :py:meth:`render_and_save`.
        :param root_dir: the root directory argument for
        :py:meth:`render_and_save`
        :param params: the parameters argument for :py:meth:`render_and_save`
        :return: the path
        """
        raise UNIMPLEMENTED_ABSTRACT_METHOD_ERROR

    @abstractmethod
    def subpath(self, params: ArchetypeParameters) -> str:
        """
        Returns the subpath, under the root directory, of the file to be
        saved by :py:meth:`render_and_save`.
        :param params: the :py:class:`ArchetypeParameters` to use as context
        when creating the subpath, e.g., when storing files whose sub-path
        might be determined by the package name.
        :return: the path
        """
        raise UNIMPLEMENTED_ABSTRACT_METHOD_ERROR

    @abstractmethod
    def render(self, params: ArchetypeParameters) -> str:
        """
        Returns the content of the file to be saved by
        :py:meth:`render_and_save`.
        :param params: the :py:class:`ArchetypeParameters` to use as context
        when building the content
        :return: the content of the file to be saved by
        :py:meth:`render_and_save`
        """
        raise UNIMPLEMENTED_ABSTRACT_METHOD_ERROR

    def render_and_save(
            self,
            root_dir: str,
            params: ArchetypeParameters
    ) -> None:
        """
        Renders and saves the content of the file and saves it the
        appropriated directory under the root directory.  The content of the
        file as well as the subpath under the root directory may be,
        but need-not be, determined by the parameters argument.
        :param root_dir: the root directory under which the file should be
        saved
        :param params: the parameters used to determine the saved file
        content and possibly the subpath under the root directory
        :return: :py:const:`None`
        """
        raise UNIMPLEMENTED_ABSTRACT_METHOD_ERROR
