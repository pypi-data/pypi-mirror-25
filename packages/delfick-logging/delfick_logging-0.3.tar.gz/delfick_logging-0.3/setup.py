from setuptools import setup

setup(
      name = "delfick_logging"
    , version = "0.3"
    , py_modules = ['delfick_logging']

    , install_requires =
      [ 'rainbow_logging_handler==2.2.2'
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
    , url = "http://github.com/delfick/delfick_logging"
    , author = "Stephen Moore"
    , author_email = "stephen@delfick.com"
    , description = "Opinionated logging helpers"
    , license = "MIT"
    )
