from setuptools import setup

setup(
    name='pyDiamondsBackground',
    author='Marco Muellner',
    author_email='muellnermarco@gmail.com',
    version='1.1.0',
    packages=['pyDiamondsBackground','pyDiamondsBackground/models'],
    licencse = 'MIT',
    description='An extension to pyDiamonds, intended for fitting pyDiamondsBackground signals of red giants',
    long_description=open('README.rst').read(),
    url='https://github.com/muma7490/PyDIAMONDS-Background',
    install_requires=[
        'numpy',
        'pyDiamonds'
    ]
)