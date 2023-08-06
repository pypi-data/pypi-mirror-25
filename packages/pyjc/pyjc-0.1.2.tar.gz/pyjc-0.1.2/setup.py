from setuptools import setup

setup(
    name='pyjc',
    version='0.1.2',
    packages=['pyjc'],
    description='An educational deep learning framework',
    url='http://github.com/Atlas7/pyjc',
    download_url='https://github.com/Atlas7/pyjc/archive/v0.1.2.tar.gz',
    author='Johnny Chan',
    author_email='johnnychan0302@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['deep learning', 'education', 'scientific computing', 'artificial intelligence'],
    python_requires='==3.6.*',
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3.2.2'],
)
