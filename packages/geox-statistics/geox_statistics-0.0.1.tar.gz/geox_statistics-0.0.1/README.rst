
https://codetrips.com/2016/09/19/how-to-publish-a-pyton-package-on-pypi/

to deploy:

.. code:: shell

    python setup.py sdist
    pip install twine
    twine upload dist/*
