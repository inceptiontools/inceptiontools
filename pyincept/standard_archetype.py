"""
standard_archetype
~~~~~~~~~~~~~~~~~~

Houses the declaration of :py:class:`TemplateArchetype` along with
supporting classes, functions, and attributes.
"""

__author__ = 'Andrew van Herick'
__copyright__ = \
    'Unpublished Copyright (c) 2020 Andrew van Herick. All Rights Reserved.'
__license__ = 'Apache Software License 2.0'

import os
from abc import ABCMeta
from enum import Enum, EnumMeta
from typing import Iterable

from pyincept.archetype import Archetype
from pyincept.archetype_parameters import ArchetypeParameters
from pyincept.template_archetype import TemplateArchetype

ARCHITYPE_DIR = os.path.abspath(
    os.path.join(
        __file__,
        os.pardir,
        'data',
        'archetypes'
    )
)


class _ABCEnumMeta(ABCMeta, EnumMeta):
    # Enables Enums to inherit from abstract base classes
    pass


class StandardArchetype(Archetype, Enum, metaclass=_ABCEnumMeta):
    """
    Enumerates the standard :py:class:`Archetype` instances available
    across the system.
    """

    APPLICATION = ('pyincept-archetype-application',)
    """
    The :py:meth:`build` method of this :py:class:`Archetype` will create a
    directory/file tree with the following structure:

    ::

        root_dir/
            my_package/
                __init__.py
                my_package.py
            tests/
                __init__.py
                end-to-end/
                    __init__.py
                    test_my_package/
                        __init__.py
                integration/
                    __init__.py
                    test_my_package/
                        __init__.py
                unit/
                    __init__.py
                    test_my_package/
                        __init__.py
            LICENSE
            Makefile
            Pipfile
            README.rst
            setup.cfg
            setup.py

    where 'root_dir' is the `root_dir argument and 'my_package' is the
    `package_name` attribute of the params argument.
    """

    def __init__(self, architype_resource_id) -> None:
        # Referencing ArchetypeBase directly for the sake of supporting Python
        # 3.5, which does not seem to handle call to super() in the context of
        # multiple inheritance as gracefully as the later versions do.
        dir_path = os.path.join(ARCHITYPE_DIR, architype_resource_id)
        self._delegate = TemplateArchetype(dir_path)

    def output_files(
            self,
            root_path: str,
            params: ArchetypeParameters
    ) -> Iterable[str]:
        return self._delegate.output_files(root_path, params)

    def build(self, root_dir: str, params: ArchetypeParameters) -> None:
        return self._delegate.build(root_dir, params)
