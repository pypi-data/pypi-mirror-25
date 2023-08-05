from setuptools import setup, find_packages

setup(
    name='easydeploy',
    version='1.1.17',
    packages=['easydeploy'],
    install_requires=[
        'Fabric3==1.13.1.post1',
        'fabtools3==0.19.0',
        'PyYAML>=3.11'
      ],
    entry_points={
        "console_scripts": [
            "ed = easydeploy.main:main",
        ]
    },
    url='https://github.com/rodrigorodriguescosta/easydeploy.git',
    license='',
    author='Rodrigo Rodrigues',
    author_email='rodrigorodriguescosta@gmail.com',
    description=''
)