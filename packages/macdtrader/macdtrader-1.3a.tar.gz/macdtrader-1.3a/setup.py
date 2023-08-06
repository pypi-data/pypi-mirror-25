#!/usr/bin/env python
from distutils.core import setup
long_description = 'generate security buy/sell signals using technical indicator MACD'
setup(name = 'macdtrader',
	version = '1.3a',
	description = 'generate security buy/sell signals using technical indicator MACD',
	maintainer = 'Thomas Thaliath',
	maintainer_email = 'tthaliath@gmail.com',
	url = 'https://github.com/tthaliath/tickerlick/tree/master/macdtrader',
	long_description = long_description,
	packages = ['macdtrader','macdtrader.test','macdtrader.cron','macdtrader.schema','macdtrader.conf'],
      	package_data={'macdtrader/test': ['*.sh'],
		      'macdtrader/cron': ['*.txt'],
		      'macdtrader/schema': ['*.sql'],
		      'macdtrader/conf': ['*.json']
 		     }
		       
	)
