from setuptools import setup, find_packages

readme = open('README.md', 'r')
readme_text = readme.read()
readme.close()

setup(
    name='cumulocity-client-python',
    version='0.0.1',
    description='UIoT Cumulocity Client',
    long_description=readme_text,
    keywords='IoT',
    author='SBD DA',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'cumulocity_client=client.main',
        ],
    }, install_requires=['paho-mqtt', 'requests']

)
