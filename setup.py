from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
reqs = [str(each.req) for each in install_reqs if each.req]


setup(
    name             = 'django-easy-response',
    version          = '1.0.1',
    author           = "Diogo Laginha",
    author_email     = "diogo.laginha.machado@gmail.com",
    url              = 'https://github.com/laginha/django-easy-response',
    description      = "Return HTTP responses in a easier way",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = reqs,
    extras_require   = {},
    zip_safe         = False,
    license          = 'MIT',
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers',
    ]
)
