from setuptools import setup, find_packages

setup(
    name='iTunesMeta',
    version='0.2.0',
    url='https://github.com/chbrown/iTunesMeta',
    author='Christopher Brown',
    author_email='io@henrian.com',
    keywords='itunes metadata',
    description='iTunes metadata extraction',
    long_description=open('README.md').read(),
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'itunes-meta = iTunesMeta.cli:main'
        ],
    },
    include_package_data=True,
)
