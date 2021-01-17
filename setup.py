from setuptools import setup, find_packages

import dictionary_crawlers

INSTALL_REQUIREMENTS = (
    'Scrapy',
)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dictionary_crawler',
    version=dictionary_crawlers.__version__,
    packages=find_packages(exclude=[]),
    include_package_data=True,
    url='https://github.com/mohammadmasoumi/dictionary_crawlers',
    license='MIT',
    author='Mohammad Masoumi',
    author_email='mohammad.masoomy74@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='A dictionary crawler written in scrapy in order to crawl longman, combridge and oxford dictionaries.',
    install_requires=INSTALL_REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
