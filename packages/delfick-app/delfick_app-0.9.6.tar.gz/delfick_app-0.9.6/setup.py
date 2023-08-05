from setuptools import setup

setup(
      name = "delfick_app"
    , version = "0.9.6"
    , py_modules = ['delfick_app']

    , install_requires =
      [ 'argparse'
      , 'delfick_error==1.7.8'
      , 'delfick_logging==0.3'
      ]

    , extras_require =
      { "tests":
        [ "noseOfYeti>=1.4.9"
        , "nose"
        , "mock"
        , "boto"
        ]
      }

    # metadata for upload to PyPI
    , url = "http://github.com/delfick/delfick_app"
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "Customized App mainline helper"
    , license = "MIT"
    )
