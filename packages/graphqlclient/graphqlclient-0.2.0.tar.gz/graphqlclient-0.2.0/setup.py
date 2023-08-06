from setuptools import setup

setup(name='graphqlclient',
      version='0.2.0',
      description='Simple GraphQL client for Python 2.7+',
      url='https://github.com/graphcool/python-graphql-client',
      author='graph.cool',
      author_email='hello@graph.cool',
      license='MIT',
      packages=['graphqlclient'],
      install_requires=[
          'six',
      ],
      zip_safe=False)
