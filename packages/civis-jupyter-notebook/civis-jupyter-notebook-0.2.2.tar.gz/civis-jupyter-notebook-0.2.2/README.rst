civis-jupyter-notebook
======================

.. image:: https://travis-ci.org/civisanalytics/civis-jupyter-notebook.svg?branch=master
    :target: https://travis-ci.org/civisanalytics/civis-jupyter-notebook

A tool to enable any Docker image to be used with Civis Platform Jupyter notebooks.

Usage
-----

In your ``Dockerfile``, put the following code at the end::

    RUN pip install civis-jupyter-notebook && \
        civis-jupyter-notebooks-install

    # Add Tini
    ENV TINI_VERSION v0.16.1
    ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
    RUN chmod +x /tini

    ENV DEFAULT_KERNEL <your kernel>  # set to one of python3, python2 or ir
    EXPOSE 8888
    WORKDIR /root/work
    ENTRYPOINT ["/tini", "--"]
    CMD ["civis-jupyter-notebooks-start"]

Here you need to replace ``<your kernel>`` with the name of your kernel (e.g.,
one of ``python2``, ``python3``, or ``ir``). Note that your Dockerfile must use
``root`` as the default user.

See the `example`_ Docker image for more details.

.. _example: example

Integration Testing Docker Images with the Civis Platform
---------------------------------------------------------

If you would like to test your image's integration with the Civis Platform locally follow the steps below:

1. Create a notebook in your Civis Platform account and grab the id of the notebook. This ID is the number
   that appears at the end of the URL for the notebook, ``https://platform.civisanalytics.com/#/notebooks/<NOTEBOOK ID>``.
2. Create an environment file called ``my.env`` and add the following to it::

    PLATFORM_OBJECT_ID=<NOTEBOOK ID>
    CIVIS_API_KEY=<YOUR CIVIS API KEY>

3. Build your image locally: ``docker build -t test .``.
4. Run the container: ``docker run --rm -p 8888:8888 --env-file my.env test``.
5. Access the notebook at the ip of your Docker host with port 8888 (e.g., ``http://localhost:8888/notebooks/notebook.ipynb``).

Integration Testing Code Changes with the Civis Platform
--------------------------------------------------------

The scripts ``tests/build_dev_image.sh`` and ``tests/run_dev_image.sh`` can be used to test the
integration of coee changes with the Civis Platform.

From the top directory in the repo type::

    $ ./test/build_dev_image.sh
    $ ./test/run_dev_image.sh <NOTEBOOK ID>

where ``<NOTEBOOK ID>`` is the ID of a Civis Platform notebook. See step 1 above if you do not
have a notebook ID. Then you can connect to the notebook from your local browser and check
to make sure it is working properly.

Contributing
------------

See ``CONTIBUTING.md`` for information about contributing to this project.

License
-------

BSD-3

See ``LICENSE.md`` for details.
