from setuptools import setup, find_packages

setup(
    name='LSHEngine',
    version='1.0.0',    
    description='This repo aims to implement an engine for Locality-Sensitive Hashing (LSH). Modules should be able to be attached to this engine in order to create specific recommendations as output from the Engine.',
    url='https://github.com/Muvels/LSHEngine',
    author='Matteo Marolt',
    author_email='',
    license='https://github.com/Muvels/LSHEngine',
    packages = find_packages(),
    install_requires=['pandas',
                      'numpy',
                      'regex'                    
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research'
    ],
)