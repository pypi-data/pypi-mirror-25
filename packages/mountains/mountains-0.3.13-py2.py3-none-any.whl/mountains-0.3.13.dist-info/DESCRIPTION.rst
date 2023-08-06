mountains
=========

|travis-ci| |Coverage Status|

A util collection for python developing.

Upload to PyPi
--------------

生成 wheel 包

::

    python setup.py bdist_wheel --universal upload

生成 tar.gz 包，因为 setup.py 用到了 pypandoc，安装的时候会需要依赖

::

    python setup.py register sdist upload

.. |travis-ci| image:: https://travis-ci.org/restran/mountains.svg?branch=master
   :target: https://travis-ci.org/restran/mountains
.. |Coverage Status| image:: https://coveralls.io/repos/github/restran/mountains/badge.svg?branch=master
   :target: https://coveralls.io/github/restran/mountains?branch=master


