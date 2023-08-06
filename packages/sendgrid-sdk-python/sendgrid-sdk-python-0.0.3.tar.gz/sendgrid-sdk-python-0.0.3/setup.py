from setuptools import setup
from sendgrid_sdk.version import __version__

setup(
    name='sendgrid-sdk-python',
    version=__version__,
    description='A Python wrapper for the SendGrid API.',
    author='Atte Valtonen',
    author_email='atte.valtonen@singa.com',
    license='MIT',
    packages=['sendgrid_sdk'],
    include_package_data=False,
    use_2to3=False,
    install_requires=[
        'sendgrid==5.2.0'
    ]
)
