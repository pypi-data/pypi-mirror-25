

Deploy
------

https://codetrips.com/2016/09/19/how-to-publish-a-pyton-package-on-pypi/

to deploy:

TODO: write about

.. code:: shell

   git tag

Create a source package:

.. code:: shell

    rm dist/*
    python setup.py sdist # for building a zip file

To upload it, first create an account here:

https://pypi.python.org/pypi/geox-statistics/0.0.1

Then, install twine and upload the source package you build before:

.. code:: shell
    pip install twine # for installation
    twine upload dist/* # for uploading the zip file
