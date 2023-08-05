ghlint
======

|build| |pypi|

Linting utility for GitHub.

Getting Started
---------------

Set the environment variables ``GITHUB_USERNAME`` and ``GITHUB_PASSWORD`` to your GitHub credentials. Alternatively, configure your username and `access token <https://github.com/settings/tokens>`_ in the ``[SETTINGS]`` section of the ``.ghlintrc`` file:

.. code-block::

    [SETTINGS]

    # GitHub username
    username=YOUR_USERNAME

    # GitHub password or personal access token
    password=YOUR_PASSWORD

Run
---

.. code-block:: sh

    pip install -r requirements.txt
    python ghlint

or

.. code-block:: sh

    pip install .
    ghlint

Tooling
-------

Using `pyenv <https://github.com/pyenv/pyenv>`_ to switch between multiple versions of Python:

.. code-block:: sh

    pyenv versions
    pyenv global 3.6.1


.. |build| image:: https://img.shields.io/travis/martinbuberl/ghlint/master.svg
    :target: https://travis-ci.org/martinbuberl/ghlint

.. |pypi| image:: https://img.shields.io/pypi/v/ghlint.svg
    :target: https://pypi.python.org/pypi/ghlint
