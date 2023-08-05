from setuptools import setup, find_packages  
  
setup(  
    name='madliar',
    version='0.1a1.dev1022',
    description='A tiny WSGI freamwork.',
    classifiers=[  
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    # install_requires=['jinja2'],
    entry_points={
        'console_scripts': [
            'madliar-manage.py=madliar.management:execute_from_command_line',
        ],
    },
    author='caoliang',
    url='https://github.com/cl-ei',
    author_email='i@caoliang.net',
    license='MIT',  
    packages=find_packages(),
    include_package_data=False,  
    zip_safe=True,  
)

