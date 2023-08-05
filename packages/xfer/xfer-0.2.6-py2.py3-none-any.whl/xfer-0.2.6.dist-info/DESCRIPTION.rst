========
git-xfer
========

Git plugin for transferring large files across servers.


Installation
============

Clone the repo and install with pip or setuptools:

.. code-block:: bash

    git clone git@github.com:bprinty/git-xfer.git
    pip install .


Configuration
=============

To add a remote server that can be used by ``git-xfer``, either use the ``config`` subcommand:


.. code-block:: bash

    git xfer config [<type>]


Or manually add the server as a git remote:

.. code-block:: bash

    git remote add <name> <url>

    git remote add server ssh://user@server.com:22/~/git-xfer.git


Note: for remote servers using a port other than 22, please use the format above in defining the remote url. ``git-xfer`` uses the port specified in the url to do transfer operations.


Usage
=====

To start tracking a file with git-xfer, use:

.. code-block:: bash

    git xfer add <file>


To remove a file from tracking with git-xfer, use:

.. code-block:: bash

    git xfer remove <file>


To delete a local file and remove it from tracking with ``git-xfer``, use:

.. code-block:: bash

    git xfer rm <file>


To list all the files currently tracked by ``git-xfer``, use:

.. code-block:: bash

    git xfer list


To list all the files currently tracked by ``git-xfer`` on a remote, use:

.. code-block:: bash

    git xfer list <remote>


To see the difference between locally tracked files and remotely tracked files, use:

.. code-block:: bash

    git xfer diff <remote>


To push locally tracked files to a remote server, use:

.. code-block:: bash

    git xfer push <remote>


To pull tracked files from a remote server, use:

.. code-block:: bash

    git xfer pull <remote>


Questions/Feedback
==================

Submit an issue in the `GitHub issue tracker <https://github.com/bprinty/git-xfer/issues>`_.


