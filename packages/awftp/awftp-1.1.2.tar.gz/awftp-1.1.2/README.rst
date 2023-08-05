awftp
=====

**A FTP-style client for HCP Anywhere File Sync & Share**

HCP Anywhere is a File Sync & Share solution created and sold by Hitachi
Data Systems. It offers a wide range of FS&S clients for Desktop computers,
Mobile devices as well as Browsers.
The lacking piece so far was a CLI client that allows to access HCP Anywhere
on devices where no GUI is available (Linux servers, for example) or for
scripting.

**awftp** tries to fill this gap by providing a look and feel as close as
possible to well-known CLI-based ftp clients. The features available
are a subset of what is offered by ftp clients, due to the functionality the
HCP Anywhere FS&S service offers through its API; some other functions in
ftp clients simply doesn't make sense for use with HCP Anywhere. On the other
hand, there are some features (*snap*, for example) not found with ftp...

**Features**

    *   Navigate the folders stored in HCP Anywhere, including Mobilized NAS,
        Shared Folders, Team Folders, Backup Folders
    *   List folders content, including deleted files/folders
    *   Store, update and retrieve files
    *   Move files and folders
    *   Undelete files/folders
    *   Create/delete folders (even recursive)
    *   Link handling:

        *   Create links to share content with others - internal/public,
            read-only, read-write, write-only
        *   List links
        *   Delete links

    *   Work with snapshots
    *   Restore files from snapshots
    *   Dynamically enables/disables features depending on the HCP Anywhere
        version connected to
    *   Authentication is Active Directory per default; if the HCP Anywhere is
        integrated a SAML IDP for authentication, the --saml parameter allows
        to select it for authentication



Dependencies
------------

You need to have at least Python 3.4.3 installed to run **awftp**.

It uses Kenneth Reitz's famous
`requests package <http://docs.python-requests.org/en/master/>`_
for communication with HCP Anywhere. And it uses
`click <http://click.pocoo.org/6/>`_ for text output, coloring and to show a
progress bar.

Documentation
-------------

To be found at `readthedocs.org <http://awftp.readthedocs.io/en/latest/>`_

Installation
------------

Install **awftp** by running::

    $ pip install awftp


-or-

get the source from `gitlab.com <https://gitlab.com/simont3/awftp>`_,
unzip and run::

    $ python setup.py install


-or-

Fork at `gitlab.com <https://gitlab.com/simont3/awftp>`_

Contribute
----------

- Source Code: `<https://gitlab.com/simont3/awftp>`_
- Issue tracker: `<https://gitlab.com/simont3/awftp/issues>`_

Support
-------

If you've found any bugs, please let me know via the Issue Tracker;
if you have comments or suggestions, send an email to `<sw@snomis.de>`_

License
-------

The MIT License (MIT)

Copyright (c) 2016-2017 Thorsten Simons (sw@snomis.de)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
