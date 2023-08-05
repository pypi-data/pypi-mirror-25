from setuptools import setup

install_requires = [ 'rdflib', 'rdflib-jsonld', 'simplejson', 'pytz', 'python-dateutil', 'PyCrypto', 'isodate' ]

setup(name='SmartAPI',
    version='1.1.0',
    author='Asema Electronics Ltd',
    author_email='python_dev@asema.com',
    platform='noarch',
    license='BSD',
    description='Smart API RDF model manipulation in Python',
    long_description="""A communication library that allows handling Smart API semantic messages as objects. Automatically handles object parsing and serialization to multiple transfer formats and offers various helper methods for the communication.""",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],
    url='http://www.smart-api.io',
    py_modules=['SmartAPI/__init__'],
    packages=['SmartAPI/agents', 'SmartAPI/common', 'SmartAPI/factory', 'SmartAPI/model', 'SmartAPI/rdf', 'SmartAPI/smartapiexceptions'],
    install_requires=install_requires
    )
