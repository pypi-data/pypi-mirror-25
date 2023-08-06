"""
intp
-------------
Simple meta interpolation.
From an ini file with variables, we do interpolation
into another ini file.

This is useful for generating configuration files.

The interpolation format:

```
From:
[section]
name = value
```

We interpolate into:

```
[config]
attribute = {section.name}
```

Resulting in:

```
[config]
attribute = value
```

"""

from setuptools import setup


setup(
    name='intp',
    version='0.1.2',
    url='https://github.com/jjmurre/intp',
    license='BSD',
    author='Jan Murre',
    author_email='jan.murre@catalyz.nl',
    description='Simple meta interpolation',
    long_description=__doc__,
    py_modules=['intp'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
    ],
    entry_points={
        "console_scripts": ['intp=intp:main'],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
