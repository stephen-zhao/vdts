import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='zhaostephen-vdts',
    version='0.1.0',
    description='A library and CLI for checking and reporting that time series data occurs at regular intervals.',
    
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    author='Stephen Zhao',
    author_email='mail@zhaostephen.com',
    
    url='https://github.com/stephen-zhao/vdts',
    project_urls={
        "Source": "https://github.com/stephen-zhao/vdts",
    },
    
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    
    keywords=[
    ],
    
    package_dir={'': 'src'},
    packages=setuptools.find_packages(
        where='src',
    ),
    entry_points={
        "console_scripts": [
            "vdts=vdts._internal.cli.main:main",
        ]
    },
    
    python_requires='>=3.6',
    install_requires=[
        'datetime-matcher',
    ],
)