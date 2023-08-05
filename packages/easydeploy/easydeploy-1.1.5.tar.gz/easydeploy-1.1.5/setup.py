from setuptools import setup, find_packages

setup(
    name='easydeploy',
    version='1.1.5',
    install_requires=[
        'Fabric>=1.8.2',
        'fabtools>=0.19.0',
        'PyYAML>=3.11'
      ],
    entry_points={
        "console_scripts": [
            "ed = main:main",
        ]
    },
    url='https://github.com/rodrigorodriguescosta/easydeploy.git',
    license='',
    author='Rodrigo Rodrigues',
    author_email='rodrigorodriguescosta@gmail.com',
    description=''
)