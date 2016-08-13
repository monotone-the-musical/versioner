
from setuptools import setup
from setuptools.command.install import install

class post_install(install):
  def run(self):
    install.run(self)
    from subprocess import call
    call(['bash', 'files/post_install.sh'])

setup(
  name='Versioner',
  version='1.0',
  url='https://github.com/monotone-the-musical/versioner',
  author='Monotone The Musical',
  author_email='monotone.the.musical@gmail.com',
  packages=['versioner'],
  install_requires=['pick'],
  license='The MIT License (MIT)',
  long_description=open('README.txt').read(),
  cmdclass={ 'install': post_install },
)

