from setuptools import setup

setup(
    name='pyDiamondsBackground',
    author='Marco Muellner',
    author_email='muellnermarco@gmail.com',
    version='1.0.0',
    packages=['background','background/models'],
    licencse = 'MIT',
    description='An extension to pyDiamonds, intended for fitting background signals of red giants',
    long_description=open('README.rst').read(),
    url='https://github.com/muma7490/PyDIAMONDS-Background',
    install_requires=[
        'numpy',
        'pyDiamonds'
    ]
)