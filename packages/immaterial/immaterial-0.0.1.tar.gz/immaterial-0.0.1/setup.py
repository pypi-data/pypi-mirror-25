# Imports from standard libraries.  # NOQA
from setuptools import find_packages, setup  # NOQA

REPO_URL = 'https://github.com/allanjamesvestal/immaterial-python/'

VERSION = '0.0.1'


setup(
    name='immaterial',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='AGPLv3',
    description='Python helper functions for the immaterial-ui framework.',
    long_description=(
        'Python helper functions for the immaterial-ui framework.'
    ),
    url=REPO_URL,
    download_url='{repo_url}archive/{version}.tar.gz'.format(**{
        'repo_url': REPO_URL,
        'version': VERSION,
    }),
    author='Allan James Vestal, The Dallas Morning News',
    author_email='newsapps@dallasnews.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[],
)
