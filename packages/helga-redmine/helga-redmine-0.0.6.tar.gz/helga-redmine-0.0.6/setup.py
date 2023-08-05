from setuptools import setup, find_packages

version = '0.0.6'

setup(name="helga-redmine",
      version=version,
      description=('redmine plugin for helga'),
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords='irc bot redmine',
      author='alfredo deza',
      author_email='contact@deza.pe',
      url='https://github.com/alfredodeza/helga-redmine',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'helga>=1.7.5',
          'treq>=15.1.0',
          'twisted',
      ],
      tests_require=[
          'pytest-twisted',
      ],
      entry_points = dict(
          helga_plugins = [
              'redmine = redmine:redmine',
          ],
      ),
)
