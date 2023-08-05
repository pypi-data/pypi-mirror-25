from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name="pdfpages", packages=["pdfpages"], version="0.1.0", install_requires=["PyPDF2"],
      include_package_data=True, scripts=["bin/pdfpages"],
      keywords=["pdf", "extract", "filter", "copy", "duplicate", "pages"],
      description="Extract pages from PDF documents", url="https://github.com/philbooth/pdfpages",
      long_description=readme(),
      download_url="https://github.com/philbooth/pdfpages/archive/0.1.0.tar.gz",
      author="Phil Booth", author_email="pmbooth@gmail.com",
      classifiers=["Development Status :: 3 - Alpha", "License :: OSI Approved :: MIT License",
                   "Natural Language :: English", "Programming Language :: Python :: 2",
                   "Natural Language :: English", "Programming Language :: Python :: 3",
                   "Topic :: Utilities"])

