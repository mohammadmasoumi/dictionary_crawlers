from setuptools import setup, find_packages

import dictionary_crawlers

INSTALL_REQUIREMENTS = (
    'Scrapy',
)

setup(
    name='dictionary_crawler',
    version=dictionary_crawlers.__version__,
    packages=find_packages(exclude=[]),
    include_package_data=True,
    url='https://github.com/mohammadmasoumi/dictionary_crawlers',
    license='MIT',
    author='Mohammad Masoumi',
    author_email='mohammad.masoomy74@gmail.com',
    description='A dictionary crawler written in scrapy in order to crawl longman, combridge and oxford dictionaries.',
    install_requires=INSTALL_REQUIREMENTS,
)
