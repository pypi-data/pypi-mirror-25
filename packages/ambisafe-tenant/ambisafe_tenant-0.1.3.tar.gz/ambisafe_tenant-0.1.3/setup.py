import os
from setuptools import setup, find_packages

__version__ = '0.1.3'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASEDIR, 'README.rst')).read()

setup(
    name='ambisafe_tenant',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=map(lambda r: r.strip(), open(os.path.join(os.path.dirname(__file__), 'requirements.txt')).readlines()),
    url='https://github.com/Ambisafe/ambisafe_tenant_client',
    download_url='https://github.com/Ambisafe/ambisafe_tenant_client/get/v{0}.zip'
        .format(__version__),
    author='Kirill Pisarev',
    author_email='kirill@ambisafe.co',
    keywords=['ambisafe', 'ethereum', 'etoken'],
    description='Ambisafe-tenant server client library',
    long_description=README,
    classifiers=[
        'Intended Audience :: Developers',
    ],
    test_suite='test.test',
    setup_requires=[
        "requests>=2.7.0",
        "python-stdnum==1.4",
        "pycoin==0.62",
        "mock>=1.3.0",
        "pysha3==0.3"
    ]
)
