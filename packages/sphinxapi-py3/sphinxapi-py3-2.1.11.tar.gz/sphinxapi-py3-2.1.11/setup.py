from setuptools import setup, find_packages

setup(
    name='sphinxapi-py3',
    version='2.1.11',
    description='Python 3 port of official python client for Sphinx Search',
    keywords='sphinxsearch',
    long_description=open('README.md').read(),
    author='Sphinx Technologies Inc.',
    url='https://github.com/atuchak/sphinxapi-py3',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
