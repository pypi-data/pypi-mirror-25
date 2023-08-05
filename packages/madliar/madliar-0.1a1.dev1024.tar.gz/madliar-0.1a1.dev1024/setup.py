from setuptools import setup, find_packages
"""
Script to build up madliar site-packages.

"""

setup(
    name='madliar',
    author='caoliang',
    url='https://github.com/cl-ei',
    author_email='i@caoliang.net',
    version='0.1a1.dev1024',
    description='A tiny WSGI freamwork.',
    license='MIT',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=True,

    # There are some problems of encoding errors to solve
    # with the built-in template, so this WSIG freamwork
    # is using jinja2 template plugin.
    # install_requires=['jinja2'],

    entry_points={
        'console_scripts': [
            'madliar-manage = madliar.management:execute_from_command_line',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
