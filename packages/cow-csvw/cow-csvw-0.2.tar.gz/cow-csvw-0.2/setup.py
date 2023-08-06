from distutils.core import setup
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

cow_base = 'src/'
cow_data = [ root.replace(cow_base, '') + '/*' for root,dirs,files in os.walk(cow_base) ]
cow_version = '0.1'

setup(
  name = 'cow-csvw',
  packages = ['cow-csvw'], # this must be the same as the name above
  package_dir = {'cow-csvw': 'src'},
  package_data = {'cow-csvw': cow_data},
  version = '0.2',
  description = 'Batch converter of large CSVs into CSVW/RDF',
  author = 'Rinke Hoekstra, Kathrin Dentler, Auke Rijpma, Richard Zijdeman, Albert Merono-Penuela',
  author_email = 'albert.merono@vu.nl',
  url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
  download_url = 'https://github.com/CLARIAH/COW/archive/0.2.tar.gz', # I'll explain this in a second
  keywords = ['csv', 'rdf', 'csvw'], # arbitrary keywords
  classifiers = [],
  install_requires=required
)
