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
