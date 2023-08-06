from setuptools import setup

setup(
    name='solat',
    version='0.1',
    description='Malaysia prayer time based on jakim XML',
    url='https://github.com/SyafiqTermizi/waktu-solat/',
    author='syafiq',
    author_email='ahmadsyafiq93@gmail.com',
    packages=['solat'],
    install_requires=[
        'xmltodict',
    ],
    zip_safe=False
)
