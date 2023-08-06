from setuptools import setup
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

name = 'pyDiamondsBackground'
version = '1.1'
release = '1.1.0'


setup(
    name=name,
    author='Marco Muellner',
    author_email='muellnermarco@gmail.com',
    version='1.1.1',
    packages=['pyDiamondsBackground','pyDiamondsBackground/models'],
    licencse = 'MIT',
    description='An extension to pyDiamonds, intended for fitting pyDiamondsBackground signals of red giants',
    long_description=open('README.rst').read(),
    url='https://github.com/muma7490/PyDIAMONDS-Background',
    install_requires=[
        'numpy',
        'pyDiamonds'
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release)}}
)