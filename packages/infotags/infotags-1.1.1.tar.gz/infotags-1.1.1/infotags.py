# coding=utf-8

"""
infotags
========

Infotags extracts package or module meta information for use by setup.py and
packaging utilities. It scans your package or module's source code for tags of
the form `__tag_name__ = literal_value`, removing the double underscores and
dropping them into a dictionary for easy access. It also captures the package or
module's name and docstring (if any) in the process. The key advantage to using
infotags is that it doesn't import your package or module, which means it can be
used even during installation when your package or module's dependencies haven't
been installed yet.


Here's an example of how to use the infotags module in your setup.py script:

    import sys
    from distutils.core import setup

    # If you don't like this try/except block, feel free to include infotags.py
    # in your distribution next to your setup.py script. Then it will be
    # guaranteed to always be available.
    try:
        import infotags
    except ImportError:
        print("The installer for this package requires the infotags module. "
              "Please install it first with 'pip install infotags'.")
        sys.exit(2)

    # Use the name you would actually use to import your package or module.
    PACKAGE_NAME = 'name_of_package_or_module'

    setup(**infotags.get_info(PACKAGE_NAME))

For a more extended example, see the setup.py script for the infotags module
itself.



This package is released under the MIT license. Full copyright/license
information for infotags:

    Copyright (c) 2015-2017 Aaron Hosford

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.
"""

import ast
import os
import parser
import warnings


# Info tags for infotags.py (how meta!)
__author__ = 'Aaron Hosford'
__author_email__ = 'hosford42@gmail.com'
__version__ = '1.1.1'
__description__ = 'Meta info extraction for Python package setup scripts'
__long_description__ = __doc__
__license__ = 'MIT (https://opensource.org/licenses/MIT)'
__url__ = 'https://github.com/SaintAttila/infotags'

__py_modules__ = [__name__]
__platforms__ = ['any']
__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',

    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',

    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Installation/Setup',
    'Topic :: System :: Software Distribution',
    'Topic :: Utilities',
]
__keywords__ = 'setuptools distutils setup meta metadata'


try:
    isidentifier = str.isidentifier
except AttributeError:
    def isidentifier(string):
        """Determine whether a string is a valid Python identifier."""
        return (
            bool(string) and
            (string[0].isalpha() or string[0] == '_') and
            all(c.isalnum() or c == '_' for c in string)
        )


def _split_entry(entry, doc):
    """
    Split an entry for extract_info().

    :param entry: The entry.
    :param doc: Whether the entry is for a docstring.
    :return: A tuple, (name, value), where name is the name of the entry, minus
        double underscores, and value is the (possibly incomplete) string
        representation of the Python literal value.
    """
    assert isinstance(entry, str)
    assert isinstance(doc, bool)

    if doc:
        return 'doc', entry.strip()

    index = entry.index('=')
    name = entry[:index].strip()
    assert name.startswith('__')
    assert name.endswith('__')
    return name[2:-2], entry[index + 1:].strip()


def is_valid_expression(source):
    """
    Determine whether the source code represents a valid Python expression.

    :param source: The string containing the source code.
    :return: Whether the source code is a valid Python expression.
    """
    # noinspection PyBroadException
    try:
        parser.expr(source)
    except Exception:
        return False
    else:
        return True


def is_valid_suite(source):
    """
    Determine whether the source code represents a valid Python "suite" (meaning
    a statement or block).

    :param source: The string containing the source code.
    :return: Whether the source code is a valid Python "suite".
    """
    # noinspection PyBroadException
    try:
        parser.suite(source)
    except Exception:
        return False
    else:
        return True


def extract_info(source_path, package_name=None):
    """
    Parse a Python source file, extracting the docstring and info tags. Put the
    results into a dictionary keyed by the info tag name (minus the double
    underscores). The docstring will be stored under key 'doc'.

    :param source_path: The path to the Python source file.
    :param package_name: The name of the package.
    :return: The info map.
    """
    results = {}
    if package_name is not None:
        results['name'] = package_name
    with open(source_path) as source_file:
        entry = None
        doc = False
        for line in source_file:
            if entry is None:
                if line[:1].isspace():
                    pass  # Info tags and docstrings must not be indented
                elif 'doc' not in results and line.startswith(('"', "'")):
                    # We may have found the docstring
                    entry = line
                    doc = True
                else:
                    # We may have found an info tag
                    index = line.find('=')
                    if index != -1 and line[index:index + 2] != '==':
                        identifier = line[:index].rstrip()
                        # It's only a valid info tag if it starts and ends with
                        # double underscores, is a valid identifier, and is all
                        # lower case. We also ignore it if it duplicates an
                        # earlier entry with the same name, since it is more
                        # likely that the entry nearer to the top of the file
                        # is the intended one.
                        if (identifier.startswith('__') and
                                identifier.endswith('__') and
                                isidentifier(identifier) and
                                identifier.lower() == identifier and
                                identifier[2:-2] not in results):
                            entry = line
            else:
                # If we have a partial entry, we should continue to add to it
                # until we determine whether we can extract info from it or not.
                entry += line

            if entry is not None:
                name, value = _split_entry(entry, doc)
                if is_valid_expression(value):
                    # If the value is an expression, then it's either a literal,
                    # or it isn't something we want to include in the results.
                    # In either case, we are done with the current entry and
                    # should start looking for a new one.
                    try:
                        value = ast.literal_eval(value)
                    except ValueError:
                        # Here we allow one special exception to the requirement
                        # that entry values must always be Python literals.
                        # They may also reference other entries. This allows us
                        # to use the following common idioms:
                        #   __long_description__ = __doc__
                        #   __package_data__ = {__name__: ['*.ini']}
                        if (value.startswith('__') and value.endswith('__') and
                                value[2:-2] in results):
                            results[name] = results[value[2:-2]]
                        else:
                            try:
                                if any(('__' + key + '__') in value
                                       for key in results):
                                    for key in sorted(results, key=len,
                                                      reverse=True):
                                        if isinstance(results[key], str):
                                            # ast.literal_eval can't handle
                                            # addition of strings, but when we
                                            # do the replace, we can get rid of
                                            # the plus and use the automatic
                                            # string-joining syntax. Because we
                                            # are still running it through
                                            # ast.literal_eval(), it's a safe
                                            # operation.
                                            pieces = value.split('__%s__' % key)
                                            for index, piece in enumerate(pieces):
                                                if piece.lstrip().startswith('+'):
                                                    piece = piece.lstrip()[1:]
                                                if piece.rstrip().endswith('+'):
                                                    piece = piece.rstrip()[:-1]
                                                pieces[index] = piece
                                            joiner = repr(results[key])
                                            value = joiner.join(pieces)
                                        else:
                                            value = value.replace(
                                                '__%s__' % key,
                                                repr(results[key])
                                            )
                                value = ast.literal_eval(value)
                            except ValueError:
                                # It's not a valid entry.
                                warnings.warn(
                                    "Ill-formed tag value for tag %s:\n%s" %
                                    (name,
                                     repr(value)[:100] +
                                     ('...' if len(repr(value)) > 100 else ''))
                                )
                            else:
                                results[name] = value
                    except SyntaxError:
                        pass  # It's not a valid entry.
                    else:
                        results[name] = value
                    entry = None
                    doc = False
                elif is_valid_suite(entry):
                    # If the entire entry is a valid "suite"  and we didn't
                    # already process it as an entry, then it is something else
                    # and we should drop it and start looking for a new entry.
                    entry = None
                    doc = False
    return results


def locate_source_files(package_name, parent_folder=None):
    """
    Locate the source files associated with a package or module.

    :param package_name: The name of the package or module.
    :param parent_folder: The path to the parent folder where the package can be
        found. By default, the CWD is checked first, and then the folder
        containing the infotags.py module is searched. The reason the folder
        containing the infotags.py module is included is so other packages can
        include infotags.py in their distribution next to the setup.py script,
        eliminating the requirement that it be installed first.
    :return: A list of source file paths. If package_name.py exists, it will
        appear first in the list. If __main__.py and/or __init__.py exist, they
        will appear in that order.
    """
    assert package_name and isinstance(package_name, str)
    assert isidentifier(package_name)

    # Find the correct parent folder.
    if not parent_folder:
        search_folders = [os.getcwd(), os.path.dirname(__file__)]
        for search_folder in search_folders:
            if (os.path.exists(os.path.join(search_folder, package_name)) or
                    os.path.exists(os.path.join(search_folder,
                                                package_name + '.py'))):
                parent_folder = search_folder
                break
        else:
            parent_folder = search_folders[0]
    else:
        assert isinstance(parent_folder, str)
    parent_folder = os.path.abspath(parent_folder)
    if not os.path.isdir(parent_folder):
        raise NotADirectoryError(parent_folder)

    # Locate the module/package source file(s) within the parent folder.
    package_path = os.path.join(parent_folder, package_name)
    source_paths = [package_path + '.py']
    for file_name in '__main__.py', '__init__.py':
        file_path = os.path.join(package_path, file_name)
        source_paths.append(file_path)
    source_paths = [source_path for source_path in source_paths
                    if os.path.isfile(source_path)]
    if not source_paths:
        raise FileNotFoundError(
            "Source file(s) for package/module %s could not be located in %s." %
            (package_name, parent_folder)
        )

    # Return the results.
    return source_paths


def get_info(package_name, parent_folder=None):
    """
    Create a dictionary containing all the information extracted from any
    identifiable source files associated with the given package name.

    :param package_name: The name of the package or module.
    :param parent_folder: The folder where the package or module can be located.
    :return:
    """
    results = {'name': package_name}
    for source_path in reversed(locate_source_files(package_name,
                                                    parent_folder)):
        results.update(extract_info(source_path, package_name))
    return results
