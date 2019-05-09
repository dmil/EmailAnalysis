from setuptools import setup

setup(name='emailanalysis',
      description='Analyze email d',
      url='https://github.com/dmil/EmailAnalysis',
      author='Dhrumil Mehta',
      author_email='dhrumil.mehta@gmail.com',
      packages=['emailanalysis'],
      install_requires=['httplib2','dateutils','blessings','html2text',
      	'peewee','oauth2client', 'google-api-python-client']
      )
