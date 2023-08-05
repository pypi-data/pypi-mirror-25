from setuptools import setup, find_packages  
  
setup(  
    name='madliar',
    version='0.1a1.dev1017',
    description='A tiny WSGI freamwork.',
    classifiers=[  
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python',  
        'Intended Audience :: Developers',  
        'Operating System :: OS Independent',  
    ],  
    author='caoliang',
    url='https://github.com/cl-ei',
    author_email='i@caoliang.net',
    license='MIT',  
    packages=find_packages(),
    include_package_data=False,  
    zip_safe=True,  
)
