from setuptools import setup

setup(
    name='jsoncut',
    author='Brian Peterson',
    author_email='bpeterso2000@yahoo.com',
    version='0.6',
    url='http://github.com/bpeterso2000/jsoncut',
    packages=['jsoncut'],
    description='A JSON inspection & pruning tool.',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['click', 'colorama', 'pygments'],
    entry_points={
        'console_scripts': ['jsoncut=jsoncut.cli:main']
    }
)
