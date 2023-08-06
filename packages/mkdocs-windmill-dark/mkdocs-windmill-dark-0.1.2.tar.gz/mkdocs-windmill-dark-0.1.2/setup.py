from setuptools import setup, find_packages

VERSION = '0.1.2'

setup(
    name="mkdocs-windmill-dark",
    version=VERSION,
    url='https://github.com/noraj1337/mkdocs-windmill-dark',
    license='MIT',
    description='MkDocs theme focused on navigation and usability',
    author='Alexandre ZANNI',
    author_email='alexandre.zanni@engineer.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'windmill-dark = mkdocs_windmill_dark',
        ]
    },
    zip_safe=False
)
