civis-jupyter-notebook
======================

.. image:: https://travis-ci.org/civisanalytics/civis-jupyter-notebook.svg?branch=master
    :target: https://travis-ci.org/civisanalytics/civis-jupyter-notebook

A tool to enable any Docker image to be used with Civis Platform Jupyter notebooks.

Usage
-----

In your ``Dockerfile``, put the following code at the end::

    ENV SHELL=/bin/bash \
        DEFAULT_KERNEL=<your kernel>

    RUN pip install civis-jupyter-notebook && \
        civis-jupyter-notebooks-install

    EXPOSE 8888
    WORKDIR /root/work
    CMD ["civis-jupyter-notebooks-start", "--allow-root"]

Here you need to replace ``<your kernel>`` with the name of your kernel (e.g.,
one of ``python2``, ``python3``, or ``ir``). Note that your Dockerfile must use
`root` as the default user.

Contributing
------------

See ``CONTIBUTING.md`` for information about contributing to this project.

License
-------

BSD-3

See ``LICENSE.md`` for details.
