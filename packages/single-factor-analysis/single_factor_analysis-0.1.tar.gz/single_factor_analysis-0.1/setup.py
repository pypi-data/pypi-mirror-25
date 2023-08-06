from setuptools import setup

setup(name='single_factor_analysis',
    version='0.1',
    description='Simple python implementation of single factor'+
    'analysis based on \"The EM Algorithm'+
    'for Mixtures of Factor Analyzers\", Hinton et al.'+
    '1997 (http://www.cs.toronto.edu/~fritz/absps/tr-96-1.pdf)',
    url='http://github.com/kdmarrett/single_factor_analysis',
    author='Karl Marrett',
    author_email='kdmarrett@gmail.com',
    license='MIT',
    install_requires=['numpy'],
    python_requires='>=3',
    packages=['single_factor_analysis'],
    zip_safe=False)
