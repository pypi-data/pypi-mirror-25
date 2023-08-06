#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name='django-requestuser',
    version=__import__('requestuser').__version__,
    description='Make current request.user available to templates',
    author='j',
    author_email='j@mailb.org',
    url='https://r-w-x.org/django-requestuser.git',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(
        exclude=['tests', 'testapp']
    ),
    include_package_data=True,
    install_requires=[
        # 'Django>=1.9', commented out to make `pip install -U` easier
    ],
    dependency_links=[
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
    zip_safe=False,
)
