from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='recarguide',
    version='0.0.1',
    description='ReCarGuide - Car Guide Application',
    long_description=readme(),
    url='https://github.com/resurtm/recarguide',
    download_url='https://github.com/resurtm/recarguide/archive/v0.0.1.tar.gz',
    author='resurtm',
    author_email='resurtm@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['recarguide'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django==1.11.6',
    ]
)
