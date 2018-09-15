import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='managr',
    version='1.0.0',
    url='http://github.com/xChenny/bankr',
    license='MIT',
    maintainer='Andrew and David Chen',
    maintainer_email='andrew.chen923@gmail.com',
    description='The Bankr web application that helps freshers learn more about how to manage their money.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask_cors',
        'flask',
        'werkzeug',
        'mongoengine'
    ],
)
