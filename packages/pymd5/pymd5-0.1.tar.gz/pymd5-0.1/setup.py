"""Setup for pymd5 module and command-line script."""
from setuptools import setup

def readme():
    """Use text contained in README.rst as long description."""
    with open('README.rst') as desc:
        return desc.read()


setup(name='pymd5',
      version='0.1',
      description=('Recursively calculate and display MD5 file hashes '
                   'for all files rooted in a directory.'),
      long_description=readme(),
      url='https://github.com/richmilne/pymd5/releases/tag/v0.1',
      author='Richard Milne',
      author_email='richmilne@hotmail.com',
      license='MIT',
      packages=['pymd5'],
      include_package_data=True,
      entry_points={
          'console_scripts': ['pymd5=pymd5:_read_args']
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
     )
