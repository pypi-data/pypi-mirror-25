from distutils.core import setup
from pip.req import parse_requirements
install_reqs = parse_requirements("requirements.txt", session="i")
requirements = [str(r.req) for r in install_reqs]
setup(
    name = 'reasoner',
    packages = [ 'graph_components' ], # this must be the same as the name above
    package_data={ "." : [ "requirements.txt" ] },
    version = '0.04',
    description = 'Reasoner common components',
    author = 'Steve Cox',
    author_email = 'scox@renci.org',
    install_requires = requirements,
    include_package_data=True,
    url = 'https://github.com/stevencox/reasoner.git',
    download_url = 'https://github.com/stevencox/reasoner/archive/0.1.tar.gz',
    keywords = [ 'biomedical', 'environmental', 'exposure', 'clinical' ],
    classifiers = [ ],
)
