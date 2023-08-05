from setuptools import setup

setup(
    name='harbor-cli',
    version='0.0.0.0',
    description='CLI for the Harbor application.',
    py_modules=['main'],
    install_requires=[
        'Click',
        'PyYaml',
        'pyrebase'
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
