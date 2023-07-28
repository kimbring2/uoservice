from distutils.core import setup

setup(
  name = 'uoservice',         
  packages = ['uoservice'],   
  package_data={
      'uoservice': ['protos/*', 'install_bash.sh'],
  },
  version = '0.0.1',      
  license='MIT',        
  description = 'Package to connect the Ultima Online C# client with Python and to parse the MPQ replay of human',   
  author = 'kimbring2',                   
  author_email = 'kimbring2@gmail.com',      
  url = 'https://github.com/kimbring2/uoservice',   
  download_url = 'https://github.com/kimbring2/uoservice',    
  keywords = ['Machine Learning', 'Deep Learning', 'MMORPG', 'Ultima Online'],   
  install_requires=[            
          'numpy',
          'pygame>=1.9.6',
          'pygame-widgets>=1.0.0',
          'mpyq',
          'opencv-python',
          'tqdm'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Science/Research',      
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.7',
  ],
)