from setuptools import setup

setup(name='bpc8583',
      version='1.1',
      
      description='BPC\'s flavour of ISO8583',
      long_description=open('README.md').read(),
      
      classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        
        'Topic :: Communications',
        'Intended Audience :: Developers',
      ],
      
      keywords='BPC\'s flavour of ISO8583 banking protocol library',
      
      url='https://github.com/timgabets/bpc8583',
      author='Tim Gabets Nikolopoulos',
      author_email='tim@gabets.ru',
      
      license='LGPLv2',
      packages=['bpc8583'],
      install_requires=['enum34', 'pycrypto'],
      zip_safe=True)