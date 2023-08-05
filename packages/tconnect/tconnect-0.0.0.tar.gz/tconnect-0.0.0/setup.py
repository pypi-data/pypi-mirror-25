from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tconnect',
    author='Maxim Schuwalow',
    author_email='maxim.schuwalow@gmail.com',
    url='https://github.com/MSchuwalow/TConnect',
    packages=['tconnect'],
    install_requires=required
)
