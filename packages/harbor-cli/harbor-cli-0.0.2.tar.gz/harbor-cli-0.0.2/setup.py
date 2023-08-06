from setuptools import setup, find_packages

setup(
    name='harbor-cli',
    version='0.0.2',
    description='Harbor-CLI is a tool to share Android builds of React Native projects',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'Click',
        'PyYaml',
        'pyrebase',
        'pyfiglet',
        'colorama',
        'pyspin',
        'requests'
    ],
    entry_points={
        'console_scripts': ['harbor=lib.cli_hooks:cli']
    },
    url='',
    author='Srishan Bhattarai',
    author_email='srishanbhattarai@gmail.com',
    license='MIT',
    include_package_data=True
)
