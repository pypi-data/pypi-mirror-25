from setuptools import setup, find_packages


setup(
    name='lu',
    version='0.1.0',
    description='单词查询工具',
    long_description='单词查询工具',
    keywords='dictionary dict word lookup terminal',
    author='taipa',
    author_email='taipa@qq.com',
    url='https://github.com/TaipaXu/lu',
    license='GPL v3.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'lu = lu.lu:main'
        ]
    }
)
