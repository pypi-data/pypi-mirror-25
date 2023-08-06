try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup
from shutil import rmtree
import os
import sys

readme = open('README.md').read()
import blinker
version = blinker.__version__

here = os.path.abspath(os.path.dirname(__file__))

class PublishCommand(Command):
    """
    Support setup.py publish.
    Graciously taken from https://github.com/kennethreitz/setup.py
    """

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _remove_builds(self, msg):
        try:
            self.status(msg)
            rmtree(os.path.join(here, 'dist'))
            rmtree(os.path.join(here, 'build'))
            rmtree(os.path.join(here, '.egg'))
            rmtree(os.path.join(here, 'slack_machine.egg-info'))
        except FileNotFoundError:
            pass

    def run(self):
        try:
            self._remove_builds("Removing previous builds…")
        except FileNotFoundError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))

        self.status("Uploading the package to PyPi via Twine…")
        os.system('twine upload dist/*')

        self._remove_builds("Removing builds…")

        sys.exit()

setup(name="blinker-alt",
      version=version,
      packages=['blinker'],
      author='Jason Kirtland',
      author_email='jek@discorporate.us',
      description='Fast, simple object-to-object and broadcast signaling',
      keywords='signal emit events broadcast',
      long_description=readme,
      license='MIT License',
      url='http://pythonhosted.org/blinker/',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.4',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.0',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          ],
      cmdclass={
        'publish': PublishCommand,
      }
)
