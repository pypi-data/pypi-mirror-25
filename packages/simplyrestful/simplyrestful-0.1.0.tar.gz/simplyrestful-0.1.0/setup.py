try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='simplyrestful',
    version='0.1.0',
    keywords='Simply ReSTful REST API',
    license='MIT',
    platforms='all',
    author='Gabriel Jose Bazan',
    author_email='gbazan@outlook.com',
    maintainer='Gabriel Jose Bazan',
    maintainer_email='gbazan@outlook.com',
    include_package_data=True,
    url='https://github.com/gabrielbazan/simply-restful/',
    download_url='https://github.com/gabrielbazan/simply-restful/',
    description='A simple framework to quickly implement ReSTful APIs.',
    long_description=open('README.txt').read(),
    packages=[
        'simplyrestful',
        'simplyrestful/models'
    ],
    install_requires=[
        'flask',
        'flask_restful',
        'sqlalchemy',
        'geoalchemy2',
        'psycopg2',
        'shapely',
        'geojson'
    ]
)
