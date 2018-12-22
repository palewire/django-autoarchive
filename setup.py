from setuptools import setup


setup(
    name='django-autoarchive',
    version='0.0.3',
    description='Django helpers for automatically archiving URLs',
    author='Ben Welsh',
    author_email='ben.welsh@gmail.com',
    url='http://www.github.com/pastpages/django-autoarchive/',
    packages=('autoarchive',),
    include_package_data=True,
    license="GPLv3",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
    ],
    install_requires=[
        'savepagenow>=0.0.12'
    ]
)
