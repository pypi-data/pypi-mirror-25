from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tconnect',
    version='0.1.0',
    author='Maxim Schuwalow',
    author_email='maxim.schuwalow@gmail.com',
    url='https://github.com/MSchuwalow/TConnect',
    packages=['tconnect'],
    install_requires=required
)
