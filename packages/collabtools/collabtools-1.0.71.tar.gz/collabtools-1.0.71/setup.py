from distutils.core import setup
setup(
  name = 'collabtools',
  packages = ['collab'],
  version = '1.0.71',
  description = 'A program for interacting with the API of Collab.',
  long_description = 'A program for interacting with the API of Collab.',
  author = 'Florian Dietz',
  author_email = 'floriandietz44@gmail.com',
  url='http://example.com',
  license = 'MIT',
  package_data={
      '': ['*.txt', # this covers both the LICENSE.txt file in this folder, and the TRUTH.txt file in the /collab/ folder
          'fibonacci/*', # this covers the data in the Docker program example folder
          'input_examples/*'], # this covers the data in the input example folder
   },
   entry_points = {
        'console_scripts': [
            'collabtools=collab.collabtools:main',
        ],
    },
    install_requires=[
        'docker',
    ],
)