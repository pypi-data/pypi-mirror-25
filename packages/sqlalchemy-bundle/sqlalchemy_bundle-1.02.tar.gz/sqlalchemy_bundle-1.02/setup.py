from distutils.core import setup
setup(
  name='sqlalchemy_bundle',
  packages=['sqlalchemy_bundle'],
  version='1.02',
  description='SqlAlchemy support for applauncher',
  author='Alvaro Garcia Gomez',
  author_email='maxpowel@gmail.com',
  url='https://github.com/maxpowel/sqlalchemy_bundle',
  download_url='https://github.com/maxpowel/sqlalchemy_bundle/archive/master.zip',
  keywords=['sql', 'alchemy', 'database'],
  classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System', 'Topic :: Utilities'],
  install_requires=['applauncher', 'SQLAlchemy', 'PyMySQL']
)
