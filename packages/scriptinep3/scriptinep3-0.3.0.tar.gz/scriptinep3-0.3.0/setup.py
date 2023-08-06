import scriptine
import os

name = "scriptinep3"
version = scriptine.__version__

class zipdist(scriptine.misc.DistutilsCommand):
    def run(self):
        from scriptine.meta import zipdist_command
        zipdist_command()

options = scriptine.misc.Options(
    name = name,
    version = version,
    author = "Oliver Tonnhofer",
    author_email = "",
    description = 'python shell scripts made easy - scriptine Ported to python 3',
    long_description=open('README.rst').read() +'\n' + open('CHANGELOG.txt').read(),
    license = 'MIT License',
    url = 'https://github.com/bouke-nederstigt/scriptine',
    classifiers=[
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      ],
    packages = ['scriptine'],
    install_requires=[
        "wrapt"
    ],
    zip_safe = False,
    cmdclass = {
        'zipdist': zipdist,
    }
)

if __name__ == '__main__':
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup
    setup(**options)
