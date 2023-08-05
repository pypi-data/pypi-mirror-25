
__name__ = 'ezdashboard'
__packages__ = ['ezdashboard']

__version__ = '0.2.1'

__description__ = 'Easy dashboard creaation from raw HTML components'
__author__ = 'oscar6echo'
__author_email__ = 'olivier.borderies@sgcib.com'
__url__ = 'https://gitlab.com/oscar6echo/ezdashboard'
__download_url__ = 'https://gitlab.com/oscar6echo/ezdashboard/repository/archive.tar.gz?ref='+__version__
__keywords__ = ['python', 'dashboard', 'jinja', 'html', 'js', 'css']
__license__ = 'MIT'
__classifiers__ = ['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'
                  ]
__include_package_data__ = True
__package_data__ = {
    'templates':
         ['templates/*.html',
          'templates/*.css'
         ]
    }

