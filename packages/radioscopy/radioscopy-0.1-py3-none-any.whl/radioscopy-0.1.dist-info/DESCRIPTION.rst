Radioscopy: a simple online radio streaming player
==================================================

Radioscopy is a simple radio streaming player. It is configured using a simple
INI configuration file and hides in your system tray.

Name
----
This program is called "radioscopy" because:

- the name needed to have "radio" in it;
- the name needed to have "py" in it, since it is written in Python;
- it is a copy of `Radiotray <http://radiotray.sourceforge.net/>`.

Feature support
---------------
As few features as possible, since the author is lazy and does not wish to fix
bugs:

- Simple configuration in an INI file;
- Hides in the systray;
- Gtk backend.

Installation
------------

You will need to install the Python 3 bindings for gobject-introspection
libraries through your distribution's package manager:

.. code-block:: bash
    # apt-get install python3-gi                 # On Debian
    # guix package -i pygobject3 python3-gobject # On GNU Guix
    # dnf install python3-gobject                # On Fedora

Radioscopy can be installed using pip:

.. code-block:: bash

    $ pip install radioscopy

Note that radioscopy does not work with Python 2.

Configuration
-------------
Radioscopy is configured using the ~/.config/radioscopy/config.ini file, which
should contain one section per radio the user may want to listen to:

[Radio:Name of my radio]
url=http://...

[Radio:Another good radio]
url=http://...

Running
-------
You may run radioscopy like so:

.. code-block:: bash

    $ radioscopy

How to contribute
-----------------
Should you want to contribute, you can just send me emails. You may want to use
"git format-patch":

.. code-block:: bash

    $ git checkout -b bug/foobar
    $ vim ...
    $ git commit -a
    $ git format-patch master
    $ git send-email --to tipecaml@gmail.com *.patch


