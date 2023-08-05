#!/usr/bin/env python

from distutils.core import setup
setup(
  name = 'postcodez',
  packages = ['postcodez'],
  version = '0.10',
  description = 'Python module for managing badly formatted UK postcode data.',
  author = 'Toby Petty',
  author_email = 'hello@tobypetty.com',
  url = 'https://github.com/woblers/postcodez',
  keywords = ['postcode', 'UK', 'london', 'data', 'clean'],
  package_data={
      'postcodez': ['london_boroughs.csv','ukpostcodes.csv'],
   },

  include_package_data=True
)
