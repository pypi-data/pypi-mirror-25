from distutils.core import setup, Extension

setup(
    name='luxem',
    version='0.0.2',
    author='Rendaw',
    author_email='rendaw@zarbosoft.com',
    packages=['luxem'],
    url='https://github.com/Rendaw/luxem-python',
    download_url='https://github.com/Rendaw/luxem-python/tarball/v0.0.2',
    description='luxem is a typed data serialization format similar to JSON.',
    long_description=open('readme.md', 'r').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    ext_modules=[
        Extension(
            '_luxem',
            sources=[
                    '_luxem.c',
                    'c/luxem_rawread.c',
                    'c/luxem_rawwrite.c',
                    'c/luxem_internal_common.c',
            ]
        )
    ]
)
