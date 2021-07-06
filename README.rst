LaTeX Doc/Docstrip Support for SCons
====================================

Introduction
------------

Writing packages for LaTeX is frequently done using the Doc_ and
Docstrip_ package.  Building the package requires passing the ``.ins``
and the ``.dtx`` files through LaTeX multiple times just like a regular
LaTeX file.  This is a job best done by a build tool.  SCons_ already
has a LaTeX scanner out of the box.  This tool simply adds the
:class:`Emitter` and :class:`Builder` to tell SCons_ how to process the
files.

Usage
-----

Once installed, to use the tool simply add

.. code::

    env = Environment(tools=["default", "dtxtools"])

to your ``SConstruct``.

.. note::   You must include the "default" tools because this tool makes
            use of them to handle the regular TeX to PDF conversion.

Then, you specify a document via

.. code::

   stys = env.ins2sty([], "mystyle.ins")
   doc = env.PDF("mystys.dtx",
                 MAKEINDEX=env["MAKEINDEX"] + " -s gind.ist")

.. note::   You should include the ``[]`` target to prevent SCons from
            constantly rebuilding the style.  The outputs are fully
            defined in the ``.ins`` file, but SCons does not like an
            unspecified default target.

Installation
------------

To install, simply copy ``sconscontrib/SCons/Tool/dtxtools`` to
``site_scons/site_tools`` in your project directory, or you can place it
in the `appropriate location`_ for your system.  For more details, check
the `SCons user's guide`_.  If you are using SCons 4 or later, you can
install using

.. code::

    python -m pip install git+https://github.com/kprussing/scons-dtxtools.git

Alternatively, you can add this project as a submodule to your git
project using

.. code::

    git submodule add <url> site_scons/site_tools/dtxtools

where ``<url>`` is the current URL of the project.

.. _Doc: https://www.ctan.org/pkg/doc
.. _Docstrip: https://www.ctan.org/pkg/docstrip
.. _SCons: http://www.scons.org
.. _`appropriate location`: https://github.com/SCons/scons/wiki/ToolsIndex#Install_and_usage
.. _`SCons user's guide`: http://scons.org/doc/production/HTML/scons-user.html
