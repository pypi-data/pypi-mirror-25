from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries',
]

setup(
    name='declaration',
    author='Jordan Ambra',
    author_email='jordan@serenitysoftware.io',
    url='https://github.com/boomletsgo/declaration',
    version='0.2.0',
    classifiers=classifiers,
    description='Base classes and fields for declarative programming, like Django ORM',
    keywords='declarative declaration metaclass',
    packages=["declaration"],
    install_requires=["six>=1.0.0", "python-dateutil>=2.5.0"],
    include_package_data=True,
    license='The Unlicense',
)
