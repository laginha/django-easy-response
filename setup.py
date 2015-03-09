from setuptools import setup, find_packages

setup(
    name             = 'easy-response',
    version          = '1.0.0',
    author           = "Diogo Laginha",
    author_email     = "diogo.laginha.machado@gmail.com",
    url              = 'https://github.com/laginha/django-easy-response',
    description      = "Return HTTP responses in a easier way",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = ['django', 'simplejson'],
    extras_require   = {},
    zip_safe         = False,
    license          = 'MIT',
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers',
    ]
)
