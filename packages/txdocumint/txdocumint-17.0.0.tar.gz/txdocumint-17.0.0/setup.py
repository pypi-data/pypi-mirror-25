from setuptools import setup

setup(
    name='txdocumint',
    version='17.0.0',
    description='Twisted Python clj-documint client implementation',
    author='Jonathan Jacobs',
    author_email='jonathan@jsphere.com',
    url='https://github.com/fusionapp/txdocumint',
    platforms='any',
    license='MIT',
    packages=['txdocumint', 'txdocumint.test'],
    test_suite='txdocumint',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'twisted>=15.5.0',
        'treq>=15.1.0',
    ],
    extras_require={
        'dev': ['pytest>=2.7.1', 'testtools>=2.0.0'],
    },
)
