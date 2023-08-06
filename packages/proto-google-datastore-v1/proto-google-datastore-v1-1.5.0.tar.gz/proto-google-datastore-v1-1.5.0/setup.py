"""A setup module for the Datastore v1 protocol definitions."""

import setuptools

install_requires = [
    'protobuf==3.0.0',
    'googleapis-common-protos==1.5.0',
]

setuptools.setup(
    name='proto-google-datastore-v1',
    version='1.5.0',
    author='Google Inc',
    author_email='gcd-discuss@google.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7'
    ],
    description=('Generated files from protocol buffers'
                 ' for Cloud Datastore v1.'),
    install_requires=install_requires,
    license='Apache',
    namespace_packages=['google'],
    packages=setuptools.find_packages(),
    url='https://github.com/GoogleCloudPlatform/google-cloud-datastore'
)
