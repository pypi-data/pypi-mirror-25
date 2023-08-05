osc clone
=========

This command creates a clone of an OBS project, copying all packages,
metadata and project configuration. If necessary, it updates the
metadata to match the new project name. For this to work correctly,
it assumes the project's name is `<distro>:<release>:<component>`:

    $ osc clone debian:jessie:main debian:stretch:main

osc fork
========

This command clones a forest of OBS projects corresponding to a single
distribution with multiple components. It copies projects, adjusting
their dependencies to match the new project names.

For this to work correctly, it assumes the project names are
`<distro>:<release>:<component>`:

     $ osc fork debian:jessie debian:stretch

Installation
============

To install osc-plugin-clone, type:

    ./setup.py install

At the moment, installing to a user's home directory isn't supported.


License
=======

This program is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License version 2
text for more details.

You should have received a copy of the GNU General Public
License along with this package; if not, write to the Free
Software Foundation, Inc., 51 Franklin St, Fifth Floor,
Boston, MA  02110-1301 USA

Authors
=======

For the list of contributors, see CONTRIBUTORS.
