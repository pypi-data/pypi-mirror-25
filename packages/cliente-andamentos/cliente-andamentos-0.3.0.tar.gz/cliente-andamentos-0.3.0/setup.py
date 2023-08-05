from setuptools import setup
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))


setup(
    name='cliente-andamentos',
    version='0.3.0',
    description='Cliente python para o sistema Andamentos',
    url='https://gitlab.com/sijnet/cliente-andamentos',
    author='Lucas Almeida Aguiar',
    author_email='lucas.tamoios@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='api andamentos processos justica',

    packages=['cliente'],

    install_requires=['requests', 'arrow'],

    extras_require={
        'dev': ['mock', 'pytest', 'pytest-cov'],
        'test': ['mock', 'pytest', 'pytest-cov'],
    },

)
