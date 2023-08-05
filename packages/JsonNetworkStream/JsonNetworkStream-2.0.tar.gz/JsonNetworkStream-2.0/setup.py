from setuptools import setup

setup(name='JsonNetworkStream',
      version='2.0',
      description='library for data streaming over the network .Can be used for sending data over network ,'\
      				'following a Json Protocol for data transfer. with additional option of peer to peer '\
      				'private key based encryption ( AES - Advanced Encryption Standard ).',
      url='http://www.github.com/SumitRana/JsonNetworkStream',
      author='Sumit Rana',
      author_email='rana.sumit93@gmail.com',
      license='General',
      packages=['client','server','secure'],
      zip_safe=False)
