from distutils.core import setup
setup(
  name = 'brmbs',
  packages = ['brmbs', 'brmbs.data', 'brmbs.preprocessing', 'brmbs.model'], 
  version = '0.11',
  description = 'MBS Securities Duration Estimation Model',
  author = 'A group of MFE students',
  author_email = 'jerry.xue.dev@gmail.com',
  url = 'https://github.com/JerryDeveloper/MBSDurationModel', 
  download_url = 'https://github.com/JerryDeveloper/MBSDurationModel/archive/0.11.tar.gz', 
  keywords = ['MBS', 'Duration'], # arbitrary keywords
  classifiers = [],
)