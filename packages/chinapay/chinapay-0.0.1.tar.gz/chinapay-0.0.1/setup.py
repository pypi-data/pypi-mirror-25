from setuptools import setup, find_packages

setup(
    name = 'chinapay',
    version = '0.0.1',
    keywords = ["chinapay", "pay"],
    description = 'chinapay python sdk',
    license = 'MIT License',
    install_requires = [
        'six',
        'requests',
        'xmltodict',
        'optionaldict',
        'python-dateutil',
    ],

    author = 'liupeng',
    author_email = 'liupeng.dalian@gmail.com',
    
    packages = find_packages(),
    platforms = 'any'
)
