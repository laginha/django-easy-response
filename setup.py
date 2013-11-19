from setuptools import setup, find_packages

setup(
    name             = 'django-simple-response',
    version          = '1.0.0',
    author           = "Diogo Laginha",
    url              = 'https://github.com/laginha/django-simple-response',
    description      = "Return HTTP responses in a easier way",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = ['django', 'simplejson'],
    extras_require   = {},
    zip_safe         = False,
)
