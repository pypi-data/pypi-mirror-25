from setuptools import setup, find_packages

setup(
    name='json_ptr',
    author='Chris Ermel',
    author_email='ermel272@gmail.com',
    version='0.0.4',
    description='An implementation of IETF RFC 6901',
    license='MIT',
    url='https://github.com/ermel272/json-ptr.git',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='JSON pointer IETF RFC 6901',
    install_requires=[],
    extras_require={
        'dev': [
            'setuptools==36.2.7',
            'sphinx==1.6.3'
        ],
        'test': [
            'nose==1.3.7',
            'coverage==4.4.1',
            'coveralls==1.2.0'
        ]
    },
    packages=find_packages(),
    py_modules=(
        'json_pointer'
    ),
    include_package_data=True
)
