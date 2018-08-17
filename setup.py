
from setuptools import setup
from setuptools.command.install import install

# new
import distutils.command.bdist_rpm
import distutils.command.install


permissions = [
  ('/usr/bin', 'vs', '(500, root, root)'),
]

class post_install(install):
  def run(self):
    install.run(self)
    from subprocess import call
    call(['bash', 'files/post_install.sh'])

class bdist_rpm(distutils.command.bdist_rpm.bdist_rpm):
  def _make_spec_file(self):
    spec = distutils.command.bdist_rpm.bdist_rpm._make_spec_file(self)
    for path, files , perm in permissions:

      ##
      # Add a line to the SPEC file to change the permissions of a
      # specific file upon install.
      #
      # example:
      #   %attr(666, root, root) path/file
      #
      spec.extend(['%attr{} {}/{}'.format(perm, path, files)])

    return spec

setup(
  name='Versioner',
  version='1.0',
  url='https://github.com/monotone-the-musical/versioner',
  author='Monotone The Musical',
  author_email='monotone.the.musical@gmail.com',
  packages=['versioner'],
  install_requires=['pick'],
  license='The MIT License (MIT)',
  long_description=open('files/rpm_description.txt').read(),
  data_files=[('/usr/local/bin/versioner/', ['files/vs.py']),
              ('/etc/versioner/', ['files/versioner.cfg']),
              ('/usr/bin', ['files/vs'])],
  cmdclass={ 'install':post_install, 'bdist_rpm':bdist_rpm }

)

