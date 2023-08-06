from setuptools import setup, find_packages
from crypto_price_rss import __version__ as version


setup(
    name='crypto-price-rss',
    version=version,
    description=('Ingest crypto prices and generate rss/atom file'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    keywords='crypto atom rss',
    author='Jon Robison',
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/crypto-price-rss',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['requests', 'Werkzeug'],
    tests_require=['tox', 'coverage', 'flake8', 'wheel'],
    test_suite='tests',
    entry_points={
        'console_scripts': ['crypto_price_rss=crypto_price_rss.cli:main'],
    }
)
