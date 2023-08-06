from setuptools import setup

setup(name='libjournal',
      version='1.0',
      description='A library that allows you to create, delete, and read journal entries',
      url='https://github.com/undystopia/libjournal',
      author='Aneesh Edara, Aviral Mishra',
      author_email='kiwipop@kiwipop.me',
      license='GNU',
      packages=['libjournal'],
      keywords = ['journal', 'libj', 'libjournal'],
      download_url = "https://github.com/undystopia/libjournal/archive/1.0.tar.gz",
      install_requires=[
          'markdown',
          'datetime'
      ],
      zip_safe=False)