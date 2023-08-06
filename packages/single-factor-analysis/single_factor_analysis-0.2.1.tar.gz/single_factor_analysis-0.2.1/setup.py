from setuptools import setup

setup(name='single_factor_analysis',
    version='0.2.1',
    description='Python implementation of factor analysis',
    long_description='Single Factor Analysis based on \"The EM Algorithm '+\
        'for Mixtures of Factor Analyzers\", Hinton et al. 1997',
    url='http://github.com/kdmarrett/single_factor_analysis',
    author='Karl Marrett',
    author_email='kdmarrett@gmail.com',
    license='MIT',
    install_requires=['numpy'],
    python_requires='>=3',
    packages=['single_factor_analysis'],
    zip_safe=False)
