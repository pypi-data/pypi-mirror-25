from distutils.core import setup
setup(
  name = 'autoD',
  packages = ['autoD'], # this must be the same as the name above
  version = '3.6.1',
  description = 'A light-weight forward auto differentiation package',
  author = 'Wei Xuan Chan',
  author_email = 'w.x.chan1986@gmail.com',
  license='MIT',
  url = 'https://github.com/WeiXuanChan/autoD', # use the URL to the github repo
  download_url = 'https://github.com/WeiXuanChan/autoD/archive/v3.6.1.tar.gz', # I'll explain this in a second
  keywords = ['differentiate', 'auto', 'forward'], # arbitrary keywords
  classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
  install_requires=['numpy'],
)
