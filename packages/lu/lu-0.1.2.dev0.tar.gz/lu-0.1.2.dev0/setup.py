"""
lu
--

lu is a CLI dictionary tool.

Installation:

.. code:: bash

    $ pip install lu


Usage:

.. code::bash

    $ lu good

"""



from setuptools import setup, find_packages

import lu


setup(
    name='lu',
    version=lu.__version__,
    description=lu.__doc__.strip(),
    long_description=__doc__,
    keywords='dictionary dict word lookup terminal',
    author='taipa',
    author_email='taipa@qq.com',
    url='https://github.com/TaipaXu/lu',
    license='GPL v3.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'lu = lu.__main__:main'
        ]
    }
)
