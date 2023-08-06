from setuptools import setup

setup(
    name='jupyter-progressbar',
    version=__import__('jupyter_progressbar').__version__,
    author='Herbert Kruitbosch',
    author_email='H.T.Kruitbosch@rug.nl',
    description=('Wrap a generator or iterator with a progress bar in Jupyter Notebooks.'),
    license='BSD',
    packages=[
        'jupyter_progressbar'
    ],
    include_package_data=True,
    install_requires=[
        'IPython>=6.0.0',
        'humanize>=0.5.1<1.0',
        'ipywidgets>=0.5.1',
    ],
    extras_require={},
    zip_safe=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
