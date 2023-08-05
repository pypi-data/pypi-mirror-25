
#!/usr/bin/python

from setuptools import setup

setup(name="pylandroid",
      version='0.0.1',
      description="A library to communicate with Worx Landroid robot mower",
      url="https://github.com/freber/pylandroid",
      license="MIT",
      author="Fredrik Silfver",
      author_email="fredrik@above.se",
      scripts=["pylandroid"],
      py_modules=["pylandroid"],
      provides=["pylandroid"],
      install_requires=[
          'requests'
      ],
      extras_require={
          'console':  ['docopt'],
      })