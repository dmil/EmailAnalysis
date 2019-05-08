from setuptools import setup

setup(name='emailanalysis',
      version='0.1',
      description='Analyze email d',
      url='https://github.com/dmil/EmailAnalysis',
      author='Dhrumil Mehta',
      author_email='dhrumil.mehta@gmail.com',
      packages=['emailanalysis'],
      install_requires=['httplib2','dateutils','blessings','html2text',
      	'peewee','authenticator','oauth2client', 'google-api-python-client']
      )
