from distutils.core import setup
from version import VERSION

setup(
    name='llamicron-weber',
    packages=['weber'],
    py_modules=["version"],
    version=VERSION,
    description='A web interface for llamicron/brewer',
    author='Luke Sweeney',
    author_email='luke@thesweeneys.org',
    url='https://github.com/llamicron/weber',
    download_url="https://github.com/llamicron/weber/archive/%s.tar.gz" % VERSION,
    keywords=['beer', 'python', 'brewing', 'web', 'Flask', 'Vue.js'],
    install_requires=[
        "brewer",
        "flask"
    ],
    classifiers=[],
)
