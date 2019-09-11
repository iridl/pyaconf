import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
   name="pyaconf",
   version="0.5.0",
   author="ikh software, inc.",
   author_email="ikh@ikhsoftware.com",
   description="Yet another config library that is built around python dictionary and supports dynamic python, json, yaml, and ini formats with inheritance.",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://bitbucket.org/ikh/pyaconf",
   packages=setuptools.find_packages(),
   classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
   ],
   python_requires = '>= 3.7',
   install_requires=[
      'pyyaml == 5.1.*',
   ],
   scripts=[
      'pyaconf2json',
      'pyaconf2yaml',
   ],
   project_urls={
        'Bug Reports': 'https://bitbucket.org/ikh/pyaconf/issues',
   },
)

