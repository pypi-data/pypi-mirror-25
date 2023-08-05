from distutils.core import setup
from i import VERSION
setup(
    name='llamicron-i',
    version=VERSION,
    description='Connect to servers',
    author='Luke Sweeney',
    author_email='luke@thesweeneys.org',
    url='https://github.com/llamicron/i',
    download_url='https://github.com/llamicron/i/archive/0.1.tar.gz',
    keywords=['ssh', 'server', 'connect'],
    install_requires=[
        'terminaltables',
    ],
    scripts=["i"]
)
